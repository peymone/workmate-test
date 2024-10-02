# Third party libraries
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
import pytest_asyncio
import pytest

# BuildIn libraries
from os import environ

# My modules
from db.base import Base


# Test URL's for database
TEST_DATABASE_URL = 'tests/cats.db'
DEFAULT_DATABASE_URL = 'db/cats.db'


@pytest.fixture(scope='module', autouse=True, name='test_db_env')
def set_test_env_var_for_db():
    """Set test database url env db/cats.db"""

    # Set ENV for database
    environ['DATABASE_URL'] = TEST_DATABASE_URL
    yield TEST_DATABASE_URL

    # Remove ENV after tests
    del environ['DATABASE_URL']


@pytest_asyncio.fixture(scope='function', autouse=False, name='session')
async def create_test_db_return_session():
    """Create test database with url db/cats.db and yield session"""

    # Create async engine
    async_engine = create_async_engine("sqlite+aiosqlite://")
    async_session = async_sessionmaker(async_engine)

    # Create database
    async with async_engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)

    # Create async session
    async with async_session() as session:
        yield session

    # Close connection after test
    await session.rollback()
    await session.flush()
    await async_engine.dispose()


@pytest.fixture(scope='function', autouse=False, name='cat_data')
def data_model_for_add_cat():
    """Set data for admin router - add_cat"""

    cat = {"name": "vasya", "age": 1, "color": "white", "breed": "eater"}
    yield cat
