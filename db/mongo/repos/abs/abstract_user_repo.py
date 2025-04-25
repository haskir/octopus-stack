from abc import abstractmethod

from db.mongo.repos.abstract_repo import AbstractRepo
from db.mongo.repos.user_model import UserModel


class AbstractAdminRepo(AbstractRepo):
    @abstractmethod
    async def exists(self, ID: int) -> bool:
        pass

    @abstractmethod
    async def remove_user(self, user_id: int) -> bool:
        pass

    @abstractmethod
    async def set_user(self, user: UserModel) -> bool:
        pass

    @abstractmethod
    async def get_all_users(self) -> list[UserModel]:
        pass

    @abstractmethod
    async def set_many(self, users: list[UserModel]):
        pass

    @abstractmethod
    async def count(self) -> int:
        pass