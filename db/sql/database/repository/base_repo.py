from typing import TypeVar, Optional, Sequence, Mapping, Any

from sqlalchemy import Select
from sqlalchemy.ext.asyncio import AsyncSession
from typing_extensions import Generic

from db.sql.database import BaseSQLModel

model = TypeVar('model', bound=BaseSQLModel)


class BaseRepo(Generic[model]):
    """ Base class for all repositories, use inheritance
    Note: I didn't commit any changes in session, you have to do it yourself
    """

    METHODS_TO_WRAP = {"create", "update", "patch", "delete", "get"}

    model: type[BaseSQLModel]

    def __init_subclass__(cls):
        """ if you don't know how to use it, just remove entire method """
        cls.model = cls.__orig_bases__[0].__args__[0]  # noqa
        for method_name in cls.METHODS_TO_WRAP:
            print(f'Doing smth with {method_name} for {cls.__name__}')
            # setattr(cls, method_name, ErrorHandler.decorate(getattr(cls, method_name)))

    @classmethod
    async def create(cls, data: dict, session: AsyncSession) -> 'model':
        """ Use to create new (new = Model().from_dict(data)) """
        sql_object: 'model' = cls.model().from_dict(data, raise_error=False)
        session.add(sql_object)
        await session.flush([sql_object])
        return sql_object

    @classmethod
    async def update(cls, ID: int | str, data: dict, session: AsyncSession, pr_key: str = "id") -> 'model':
        """ Use to update existing (existing.update(data)) """
        obj: model = await cls.get(pr_key, ID, session)
        if not obj:
            raise ValueError(f"Object {cls.model.model_name} not found")
        obj.from_dict(data)
        await session.commit()
        await session.refresh(obj)
        return obj

    @classmethod
    async def patch(cls, ID: int | str, data: dict, session: AsyncSession) -> 'model':
        """ Not ready """
        return await cls.update(ID, data, session=session)

    @classmethod
    async def delete(cls, ID: int, session: AsyncSession) -> None:
        """ Use to delete existing (existing.delete()) """
        query: Select = Select(cls.model).filter_by(id=ID)
        obj = (await session.execute(query)).scalars().first()
        if not obj:
            raise ValueError(f"Object {cls.model.model_name} not found")
        await session.delete(obj)

    @classmethod
    async def get_all(cls, session: AsyncSession, filters: Mapping[str, Any] = None) -> list['model'] | Sequence['model']:
        """ Use to get all existing (all()) with filters """
        query: Select = Select(cls.model)
        if filters:
            query = query.filter_by(**filters)
        return (await session.execute(query)).scalars().all()

    @classmethod
    async def get(cls, arg, value, session: AsyncSession) -> Optional['model']:
        """ Use to get one existing (get()) """
        query: Select = Select(cls.model).filter_by(**{arg: value})
        obj: 'model' = (await session.execute(query)).scalar_one_or_none()
        return obj
