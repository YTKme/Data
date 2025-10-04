"""
Database Module
~~~~~~~~~~~~~~~
"""

import os
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy import Engine
from sqlalchemy import URL
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine

import tealogger


CURRENT_MODULE_PATH = Path(__file__).parents[1].expanduser().resolve()

# Configure conftest_logger
tealogger.configure(configuration=CURRENT_MODULE_PATH / "tealogger.json")
database_logger = tealogger.get_logger(name="database")


def initialize_database_async(
    drivername: str,
    username: str,
    password: str,
    host: str = "",
    port: int = 5432,
    database_name: str = "",
    echo: bool = False,
) -> Engine:
    """Initialize Database Asynchronous

    :param drivername: The name of the database backend
    :type drivername: str
    :param username: The username for the database connection
    :type username: str
    :param password: The password for the database connection
    :type password: str
    :param host: The host for the database connection
    :type host: str
    :param port: The port for the database connection
    :type port: int
    :param database_name: The name of the database, defaults to
        "borealis"
    :type database_name: str
    :param echo: Determine whether log output should be enabled,
        defaults to False
    :type echo: bool, optional
    :return: The engine instance for the database connection
    :rtype: Engine
    """

    database_logger.debug("Initialize Database Asynchronous")

    connection_url = URL.create(
        drivername=drivername,
        username=username,
        password=password,
        host=host,
        port=port,
        database=database_name,
    )

    engine = create_async_engine(connection_url, echo=echo)

    return engine


def initialize_database(
    drivername: str,
    username: str,
    password: str,
    host: str,
    port: int,
    database_name: str,
    echo: bool = False,
) -> Engine:
    """Initialize Database

    :param drivername: The name of the database backend
    :type drivername: str
    :param username: The username for the database connection
    :type username: str
    :param password: The password for the database connection
    :type password: str
    :param host: The host for the database connection
    :type host: str
    :param port: The port for the database connection
    :type port: int
    :param database_name: The name of the database
    :type database_name: str
    :param echo: Determine whether log output should be enabled,
        defaults to False
    :type echo: bool, optional
    :return: The engine instance for the database connection
    :rtype: Engine
    """

    database_logger.debug("Initialize Database")

    connection_url = URL.create(
        drivername=drivername,
        username=username,
        password=password,
        host=host,
        port=port,
        database=database_name,
    )

    engine = create_engine(connection_url, echo=echo)

    return engine


def get_database_session_async() -> async_sessionmaker[AsyncSession]:
    """Get Database Session Async"""

    database_logger.info("Get Database Session Asynchronous")

    username = os.environ.get("DATABASE_USERNAME")
    password = os.environ.get("DATABASE_PASSWORD")
    host = os.environ.get("DATABASE_HOST", "example.com")

    engine = initialize_database_async(
        drivername="postgresql+asyncpg",
        username=username,
        password=password,
        host=host,
        echo=True,
    )

    # async_sessionmaker: A factory for new AsyncSession objects
    # expire_on_commit: Don't expire objects after transaction commit
    async_session = async_sessionmaker(
        bind=engine,
        expire_on_commit=False,
    )

    return async_session
