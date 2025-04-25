from functools import wraps

from db.sql.database import async_session_factory


async def get_session():
    """ Yields session """
    async with async_session_factory() as session:
        yield session


def connection(method):
    """ Session decorator """
    @wraps(method)
    async def wrapper(*args, **kwargs):
        async with async_session_factory() as session:
            try:
                if "session" in kwargs:
                    return await method(*args, **kwargs)
                return await method(*args, session=session, **kwargs)
            except Exception as e:
                await session.rollback()
                raise e

    return wrapper


__all__ = [
    "connection",
    "get_session",
]
