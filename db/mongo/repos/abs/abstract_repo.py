from abc import ABC, abstractmethod


class AbstractRepo(ABC):
    @abstractmethod
    async def ensure_collection(self):
        pass

    @abstractmethod
    async def load_test_data(self):
        pass
