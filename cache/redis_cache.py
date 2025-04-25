import json
import sys
from typing import Type

from loguru import logger
from pydantic import BaseModel
from redis.asyncio import Redis

from cache import AbstractCache, Seconds
from cache.schemas import AbstractScheme, schemas
from settings import RedisSettings


class RedisCache(AbstractCache):
    _redis: Redis
    _default_expire: Seconds = 120

    def __init__(self, settings: RedisSettings):
        self._settings = settings

    async def connect(self):

        try:
            self._redis = await Redis.from_url(self._settings.redis_url)
            if not await self._redis.ping():
                sys.exit("Failed to connect to Redis")
        except Exception as e:
            logger.error(f"Failed to connect to Redis: {e}")
            raise

    async def close(self):
        if self._redis:
            await self._redis.close()

    async def get[T](self, key: str | int, model: Type[BaseModel]) -> T | None:
        scheme: AbstractScheme = schemas.get(model)
        if not scheme:
            raise NotImplementedError(f"Scheme not found for {model.__name__}")
        raw = await self._redis.get(scheme.getter(key))
        return scheme.load(raw)

    async def set(self, obj: BaseModel):
        scheme: AbstractScheme = schemas.get(obj.__class__)
        if not scheme:
            raise NotImplementedError(f"Scheme not found for {obj.__class__}")
        await self._redis.set(
            scheme.get_key(obj),
            scheme.dump(obj),
            ex=scheme.expire(obj),
        )

    async def set_many(self, objs: list[BaseModel]):
        if not objs:
            return
        scheme: AbstractScheme = schemas.get(objs[0].__class__)
        if not scheme:
            raise NotImplementedError(f"Scheme not found for {objs[0].__class__}")
        await self._redis.mset(
            {scheme.get_key(obj): scheme.dump(obj) for obj in objs},
        )
        for obj in objs:
            await self._redis.expire(scheme.get_key(obj), scheme.expire(obj))

    async def exists(self, obj: BaseModel) -> bool:
        scheme: AbstractScheme = schemas.get(obj.__class__)
        if not scheme:
            raise NotImplementedError(f"Scheme not found for {obj.__name__}")
        return bool(await self._redis.exists(scheme.getter(obj)))

    async def delete(self, model: BaseModel):
        scheme: AbstractScheme = schemas.get(model.__class__)
        if not scheme:
            raise NotImplementedError(f"Scheme not found for {model.__class__}")
        await self._redis.delete(scheme.get_key(model))

    async def clear(self):
        await self._redis.flushdb()

    async def dispose(self):
        await self._redis.close()

    async def get_all(self, model: Type[BaseModel]) -> list[BaseModel]:
        scheme: AbstractScheme = schemas.get(model)
        if not scheme:
            raise NotImplementedError(f"Scheme not found for {model.__name__}")
        ids = await self._redis.keys(scheme.get_all())
        return [scheme.load(obj) for obj in await self._redis.mget(ids)]

    async def get_all_keys(self) -> list[str]:
        return [k.decode() for k in await self._redis.keys()]

    async def get_raw(self, key: str) -> dict:
        data = await self._redis.get(key)
        if not data:
            return dict()
        return json.loads(await self._redis.get(key))