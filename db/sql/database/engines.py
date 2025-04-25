from sqlalchemy import create_engine, Engine
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession
from sqlalchemy_utils import database_exists, create_database

from db.sql.database.base_model import Base
from settings import SQLSettings, project_settings


def init_models(engine: Engine, drop: bool):
    """ Creates tables in the DB. """
    with engine.begin() as sync_session:
        if drop:
            Base.metadata.drop_all(sync_session)
        Base.metadata.create_all(sync_session)


def create_database_if_not_exist(settings: SQLSettings):
    """ Creates DB if it doesn't exist. """
    engine = create_engine(url=settings.sync_database_url)
    if not database_exists(engine.url):
        create_database(engine.url)
    init_models(engine, drop=settings.DROP_DB)


create_database_if_not_exist(settings=project_settings)
sync_engine = create_engine(project_settings.sync_database_url)
async_engine = create_async_engine(project_settings.async_database_url)
async_session_factory = async_sessionmaker(async_engine, class_=AsyncSession, expire_on_commit=False)
