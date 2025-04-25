import json

from messaging.rabbitmq import Consumer
from messaging.rabbitmq.consumer import RabbitMQConfig
from settings import project_settings

test_config = RabbitMQConfig(
    exchange="test_exchange",
    queue="test_queue",
    routing_key="test_routing_key",
)


def deserialize(data: str) -> dict:
    return json.loads(data)


class SomeService:
    @staticmethod
    async def handle_message(data: dict) -> None:
        print("Message received:", data)


async def main():
    async def stop(seconds: int = 10):
        await asyncio.sleep(10)
        await consumer.stop()

    service = SomeService()
    consumer = Consumer[dict](
        app_config=project_settings,
        rabbit_config=test_config,
        message_handler=service.handle_message,
        deserializer=deserialize,
    )
    asyncio.create_task(stop())
    await consumer.connect()


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
