import asyncio
from dataclasses import dataclass
from typing import Callable, Any

from aio_pika import connect_robust, ExchangeType
from aio_pika.abc import AbstractIncomingMessage, AbstractRobustConnection
from loguru import logger

from settings.project_settings import RabbitMQSettings


@dataclass(slots=True)
class RabbitMQConfig:
    queue: str
    exchange: str
    routing_key: str


class Consumer[T]:
    connection: AbstractRobustConnection | None

    def __init__(self,
                 app_config: [RabbitMQSettings],
                 rabbit_config: RabbitMQConfig,
                 message_handler: Callable[[T], Any],
                 deserializer: Callable[[str], T]):
        self.app_config = app_config
        self.rabbit_config = rabbit_config
        self.message_handler = message_handler
        self.deserializer = deserializer
        self.connection = None

    async def connect(self, max_retries: int = 5, retry_delay: float = 2.0):
        """ Connect to RabbitMQ with retries. """
        tries = 0
        while tries <= max_retries:
            tries += 1
            try:
                #
                connection_task = asyncio.create_task(connect_robust(
                    url=self.app_config.rabbitmq_url,  # type: ignore
                    login=self.app_config.RABBITMQ_USER,  # type: ignore
                    password=self.app_config.RABBITMQ_PASSWORD  # type: ignore
                ))
                timeout_task = asyncio.create_task(asyncio.wait_for(connection_task, 5))
                try:
                    await timeout_task
                except asyncio.TimeoutError:
                    raise TimeoutError(f"Failed to connect to RabbitMQ, timeout")
                else:
                    self.connection = connection_task.result()
                    break
            except Exception as e:
                logger.warning(f"Connection attempt {tries}/{max_retries} failed: {e}")
                if tries < max_retries:
                    await asyncio.sleep(retry_delay)
                else:
                    logger.error(f"Max retries reached. Failed to connect Consumer[{self.rabbit_config.queue}].")
                    raise

        async with self.connection:
            channel = await self.connection.channel()
            await channel.set_qos(prefetch_count=1)

            exchange = await channel.declare_exchange(self.rabbit_config.exchange, ExchangeType.DIRECT)
            queue = await channel.declare_queue(self.rabbit_config.queue, durable=True)
            await queue.bind(exchange, routing_key=self.rabbit_config.routing_key)

            logger.info(f"[Consumer] {self.rabbit_config.queue} connected successfully.")

            async for message in queue:  # type: ignore
                await self._process_message(message)

    async def _process_message(self, message: AbstractIncomingMessage):
        """ Processes incoming message and calls async message handler. """
        try:
            await message.ack()  # Подтверждаем обработку
            decoded_message = self._translate(message)
            await self.message_handler(decoded_message)
        except Exception as e:
            logger.error(f"Error processing message in {self.rabbit_config.queue} {e}")

    def _translate(self, message: AbstractIncomingMessage) -> T:
        return self.deserializer(message.body.decode())

    async def stop(self):
        """ Stops the consumer and closes the connection to queue. """
        if self.connection:
            await self.connection.close()

    @property
    def is_alive(self) -> bool:
        return self.connection is not None


__all__ = [
    "RabbitMQConfig",
    "Consumer",
]
