from abc import ABC, abstractmethod
from typing import Type

from pydantic import BaseModel

from cache.cachable import Cachable

Seconds = int


class AbstractCache(ABC):
    @abstractmethod
    async def connect(self, *args, **kwargs):
        pass

    @abstractmethod
    async def get[T](self, key: str | int, model: Type[BaseModel | Cachable]) -> T:
        pass

    @abstractmethod
    async def set(self, obj: BaseModel | Cachable) -> None:
        pass

    @abstractmethod
    async def set_many(self, objs: list[BaseModel | Cachable]) -> None:
        pass

    @abstractmethod
    async def exists(self, obj: BaseModel | Cachable) -> bool:
        pass

    @abstractmethod
    async def delete(self, model: BaseModel | Cachable) -> None:
        pass

    @abstractmethod
    async def clear(self) -> None:
        pass

    @abstractmethod
    async def get_all[T](self, model: Type[BaseModel | Cachable]) -> list[T]:
        pass

    @abstractmethod
    async def get_all_keys(self) -> list[str]:
        pass

    @abstractmethod
    async def get_raw(self, key: str) -> dict:
        pass