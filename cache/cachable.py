from abc import ABC, abstractmethod


class Cachable(ABC):
    @abstractmethod
    def to_dict(self) -> dict:
        pass

    @classmethod
    @abstractmethod
    def from_dict(cls, data: dict) -> 'Cachable':
        pass

    @abstractmethod
    def to_json(self) -> str:
        pass

    @classmethod
    @abstractmethod
    def from_json(cls, data: str) -> 'Cachable':
        pass