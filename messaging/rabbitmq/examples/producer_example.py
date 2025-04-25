import json

from messaging.rabbitmq import Producer
from messaging.rabbitmq.consumer import RabbitMQConfig
from settings import project_settings

test_config = RabbitMQConfig(
    exchange="test_exchange",
    queue="test_queue",
    routing_key="test_routing_key",
)


def serialize(data: dict) -> str:
    return json.dumps(data)


async def main():
    producer = Producer[dict](app_config=project_settings, rabbit_config=test_config, serializer=serialize)
    await producer.connect()
    await producer.send({"test": "test"})
    await producer.stop()


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
