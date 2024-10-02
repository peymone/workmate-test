# Third party libraries
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import declarative_base, Mapped, mapped_column

# BuildIn libraries
from os import path, getenv


def configurate_database() -> tuple:
    """Configurate database by creating engine, session and declarative base class"""

    # Try to set database url from env variable
    DATABASE_URL = getenv('DATABASE_URL')
    if DATABASE_URL is None:
        DATABASE_URL = 'db/cats.db'

    # Configurate sqlalchemy
    engine = create_async_engine("sqlite+aiosqlite:///" + DATABASE_URL)
    async_session = async_sessionmaker(engine)
    Base = declarative_base()

    return DATABASE_URL, engine, async_session, Base


# Configuration settings
DATABASE_URL, engine, async_session, Base = configurate_database()


class Cat(Base):
    """Schema for cats table"""

    __tablename__ = 'cats'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True, index=True)
    age: Mapped[int]
    color: Mapped[str]
    breed: Mapped[str] = mapped_column(index=True)


async def get_session() -> AsyncSession:
    """Get async session for FastAPI

    Returns:
        AsyncSession: async session
    """

    async with async_session() as session:
        return session


async def create_db() -> tuple[int, str]:
    """Create database with defined schemas

    Returns:
        tuple[int, str]: result code (0 - already exists, 1 - created), description
    """

    if path.exists(DATABASE_URL) is True:
        return (0, "Database already exists")
    else:
        async with engine.begin() as connection:
            await connection.run_sync(Base.metadata.create_all)

        return (1, 'Database created')
