from abc import ABC, abstractmethod
from typing import Type

from pydantic import BaseModel

from lib.models import Cachable


class AbstractScheme[T](ABC):
    model: Type[BaseModel]
    key: str

    def __init_subclass__(cls, **kwargs):
        if not cls.model:
            raise NotImplementedError("model is required")
        if not cls.key:
            raise NotImplementedError("key is required")

    @classmethod
    @abstractmethod
    def expire(cls, obj: T) -> int:
        """ Return the expiration time in seconds """
        pass

    @classmethod
    @abstractmethod
    def get_key(cls, obj: T) -> str:
        """ Return the key of the object """
        pass

    @classmethod
    def load(cls, serialized_obj_data: str) -> T | None:
        """ Return the object from the serialized data """
        if not serialized_obj_data:
            return None
        if issubclass(cls.model, BaseModel):
            return cls.model.model_validate_json(serialized_obj_data)
        if issubclass(cls.model, Cachable):
            return cls.model.from_json(serialized_obj_data)
        raise NotImplementedError(f"Scheme not found for {cls.model.__name__}")

    @classmethod
    @abstractmethod
    def dump(cls, obj: T) -> str:
        pass

    @classmethod
    def getter(cls, ID: int | str | T):
        if isinstance(ID, (int, str)):
            return f'{cls.key}:{ID}'
        return cls.get_key(ID)

    @classmethod
    def get_all(cls):
        return f'{cls.key}:*'
