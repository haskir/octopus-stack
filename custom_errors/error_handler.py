import asyncio
from functools import wraps

from loguru import logger

from custom_errors.errors import *


class ErrorHandler:
    @staticmethod
    def log(func, e, *args, **kwargs):
        text = f'{e.__class__.__name__}: {e}\n{func = }\n'
        if args:
            text += f'{args = }\n'
        if kwargs:
            text += f'{kwargs = }\n'
        logger.error(text)

    @classmethod
    def decorate(cls, func):
        @wraps(func)
        async def async_wrapper(*args, **kwargs) -> ErrorDTO:
            try:
                return await func(*args, **kwargs)
            except MyError as e:
                return ErrorDTO.factory(e)
            except Exception as e:
                cls.log(func, e, *args, **kwargs)
                return ErrorDTO.factory(e)

        @wraps(func)
        def sync_wrapper(*args, **kwargs) -> ErrorDTO:
            try:
                return func(*args, **kwargs)
            except MyError as e:
                return ErrorDTO.factory(e)
            except Exception as e:
                cls.log(func, e, *args, **kwargs)
                raise

        # Для асинхронной функции
        if asyncio.iscoroutinefunction(func):
            return async_wrapper
        # Для синхронной функции
        return sync_wrapper
