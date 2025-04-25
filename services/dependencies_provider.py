from loguru import logger

from cache import AbstractCache
from messaging import Producer, Consumer
from services.abs import AbstractService


class DependenciesProvider:
    """ Service objects handler """

    services: list[AbstractService]
    mongo_repos: list
    cache: AbstractCache
    rabbits: list[Consumer | Producer]

    def __init__(self):
        pass

    async def post_init(self):
        for service in self.services:
            try:
                await service.initialize()
            except Exception as e:
                logger.error(f"Failed to initialize service {service.__class__.__name__}: {e}")
        for rabbit in self.rabbits:
            try:
                await rabbit.connect()
            except Exception as e:
                logger.error(f"Failed to connect rabbit {rabbit.__class__.__name__}: {e}")

    async def dispose(self):
        logger.info("Disposing services...")
        for service in self.services:
            try:
                await service.dispose()
            except Exception as e:
                logger.error(f"Failed to dispose service {service.__class__.__name__}: {e}")
        for rabbit in self.rabbits:
            await rabbit.stop()


dp = DependenciesProvider()
