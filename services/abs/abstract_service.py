from abc import ABC, abstractmethod


class AbstractService(ABC):
    @abstractmethod
    async def initialize(self):
        pass

    @abstractmethod
    async def dispose(self):
        pass