import asyncio

from db.mongo.mongo_client import MongoClient
from db.mongo.repos.abs.abstract_user_repo import AbstractAdminRepo
from db.mongo.repos.user_model import UserModel


class AdminRepo(AbstractAdminRepo, MongoClient):
    async def exists(self, ID: int) -> bool:
        return await self.collection.find_one({"_id": ID})

    async def get_by_username(self, username: str) -> UserModel | None:
        document = await self.collection.find_one({"username": username})
        if document is None:
            return None
        return UserModel.model_validate(document)

    async def add_user(self, user: UserModel) -> bool:
        if await self.exists(user.id):
            return False
        res = await self.collection.insert_one(user.model_dump(by_alias=True))
        return res.acknowledged

    async def set_many(self, users: list[UserModel]):
        await self.collection.insert_many(
            [user.model_dump(by_alias=True) for user in users],
            ordered=False
        )

    async def remove_user(self, user_id: int) -> bool:
        if not await self.exists(user_id):
            return False
        res = await self.collection.delete_one({"_id": user_id})
        return res.deleted_count > 0

    async def get_all_users(self) -> list[UserModel]:
        documents = await self.collection.find({}).to_list()
        return [UserModel.model_validate(doc) for doc in documents]

    async def set_user(self, user: UserModel) -> bool:
        if not await self.exists(user.id):
            return await self.add_user(user)
        result = await self.collection.update_one(
            {"_id": user.id},
            {"$set": user.model_dump(by_alias=True)}
        )
        return result.modified_count > 0

    async def ensure_collection(self):
        await super().ensure_collection()
        if self.settings.DROP_DB:
            await self.collection.delete_many({})
        await self.load_test_data()

    async def load_data(self):
        admins = [
            ...,
            ...,
            ...,
        ]
        await asyncio.gather(*[self.add_user(user) for user in admins])

    async def count(self) -> int:
        return await self.collection.count_documents({})
