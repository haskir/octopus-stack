import asyncio
from dataclasses import dataclass
from typing import Callable, Any

from aio_pika import connect_robust, Message, ExchangeType, Connection, Channel, Exchange
from loguru import logger

from settings import RabbitMQSettings


@dataclass(slots=True)
class RabbitMQConfig:
    queue: str
    exchange: str
    routing_key: str


class Producer[T]:
    def __init__(self, app_config: [RabbitMQSettings], rabbit_config: RabbitMQConfig, serializer: Callable[[T], Any]):
        self.app_config = app_config
        self.rabbit_config = rabbit_config
        self.serializer = serializer
        self.connection: Connection | None = None
        self.channel: Channel | None = None
        self.exchange: Exchange | None = None

    async def connect(self, max_retries: int = 5, retry_delay: float = 2.0) -> None:
        """ Connect to RabbitMQ with retries. """
        tries = 0
        while tries <= max_retries:
            tries += 1
            try:
                logger.info(f"Attempt {tries}/{max_retries} to connect Producer...")
                self.connection = await connect_robust(
                    url=self.app_config.rabbitmq_url,  # type: ignore
                    login=self.app_config.RABBITMQ_USER,  # type: ignore
                    password=self.app_config.RABBITMQ_PASSWORD  # type: ignore
                )
                self.channel = await self.connection.channel()
                self.exchange = await self.channel.declare_exchange(
                    self.rabbit_config.exchange, ExchangeType.DIRECT
                )
                logger.info(f"Producer[{self.rabbit_config.routing_key}] connected successfully.")
                break
            except Exception as e:
                logger.warning(f"Connection attempt {tries}/{max_retries} failed: {e}")
                if tries < max_retries:
                    await asyncio.sleep(retry_delay)
                else:
                    logger.error("Max retries reached. Failed to connect Producer.")
                    raise

    async def stop(self) -> None:
        """ Stops the producer and closes the connection to queue."""
        if self.connection:
            await self.connection.close()
            logger.info("Producer connection closed.")
        self.connection = None
        self.channel = None
        self.exchange = None

    async def send(self, data: T) -> None:
        """ Sends a message to queue. """
        if not self.connection or not self.exchange:
            logger.warning("Producer is not connected. Attempting to reconnect...")
            await self.connect()

        encoded_message = self.serialize(data)
        try:
            await self.exchange.publish(
                Message(encoded_message.encode()),
                routing_key=self.rabbit_config.routing_key
            )
            logger.debug(f"Message sent: {data}")
        except Exception as e:
            logger.error(f"Failed to send message: {e}", exc_info=True)
            raise

    def serialize(self, data: T) -> str:
        """ Prepares data for sending. """
        try:
            return self.serializer(data)
        except Exception as e:
            logger.error(f"Error serializing data in Producer: {e} {data}", exc_info=True)
            raise


__all__ = [
    "RabbitMQConfig",
    "Producer",
]
