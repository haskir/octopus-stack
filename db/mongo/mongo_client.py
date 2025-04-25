from abc import abstractmethod
from typing import Type

from pydantic import BaseModel
from pymongo import AsyncMongoClient
from pymongo.asynchronous import database, collection
from pymongo.asynchronous.collection import AsyncCollection

from settings import MongoSettings


class MongoClient[T]:
    """ Base class for mongo client, provides basic functionality """
    _c: AsyncMongoClient
    db: database
    collection: AsyncCollection
    model: Type[BaseModel]
    settings: MongoSettings

    def __init__(
            self,
            client: AsyncMongoClient,
            collection_name: str,
            model: Type[BaseModel],
            settings: MongoSettings,
    ):
        self._c: AsyncMongoClient = client
        self.settings = settings
        self.db: database = client[settings.MONGO_DB]
        self.collection: AsyncCollection = self.db[collection_name]
        self.model: Type[BaseModel] = model

    async def ensure_collection(self):
        """ Use this method in child classes for creating collection and setting up indexes """
        collections = await self.db.list_collection_names()
        if self.collection.name not in collections:
            await self.db.create_collection(self.collection.name)

    @abstractmethod
    async def load_data(self):
        """ Use this method in child classes for loading data, for test purposes """
        pass


__all__ = [
    "MongoClient",
    "AsyncMongoClient",
    "database",
    "collection"
]
