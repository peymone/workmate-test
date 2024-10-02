# Third party libraries
from sqlalchemy.ext.asyncio import AsyncSession

# BuildIn libraries
from os import remove
from os.path import exists
from asyncio import run

# My modules
from db.base import configurate_database, get_session, create_db


def test_configurate_database_result_length():
    assert len(configurate_database()) == 4, "Configuration function must return tuple with 4 objects"


def test_configurate_database_env_db_variable(test_db_env):
    assert configurate_database()[0] == test_db_env, f"database url is not equal to set env variable: {test_db_env}"


def test_get_session_instanse_check():
    sesion = run(get_session())
    assert isinstance(sesion, AsyncSession) == True, "Session must be instanse of AsyncSession"


def test_create_db_path_exist():

    DEFAULT_DATABASE_URL = 'db/cats.db'
    creation_code = run(create_db())[0]

    assert creation_code == 1, "database does not created"
    assert exists(DEFAULT_DATABASE_URL) == True, f"{DEFAULT_DATABASE_URL} does not exists"

    remove(DEFAULT_DATABASE_URL)
