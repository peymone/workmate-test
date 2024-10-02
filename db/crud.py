from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete

from .base import Cat


async def add_cat(session, name: str, age: int, color: str, breed: str) -> None:
    """Add new cat to databse

    Args:
        session (AsyncSession): async session object
        name (str): cat's name
        age (int): cat's age
        color (str): cat's fur color
        breed (str): cat's breed
    """

    new_cat = Cat(name=name, age=age, color=color, breed=breed)
    session.add(new_cat)


async def update_cat(session: AsyncSession, old_name: str, name: str, age: int, color: str, breed: str) -> None:
    """Update cat with new data

    Args:
        session (AsyncSession): async session object
        old_name (str): cat's old name
        name (str): cat's new name
        age (int): cat's new age
        color (str): cat's new fur color
        breed (str): cat's new breed
    """

    statement = update(Cat).where(Cat.name == old_name).values(name=name, age=age, color=color, breed=breed)
    await session.execute(statement)


async def delete_cat(session: AsyncSession, name: str) -> None:
    """Delete cat by passing cat's name

    Args:
        session (AsyncSession): async session object
        name (str): cat's name
    """

    statement = delete(Cat).where(Cat.name == name)
    await session.execute(statement)


async def get_cats(session: AsyncSession, breed: str | None, name: str | None) -> Cat:
    """Get all cats from database OR with specific breed OR only one cat with specific name

    Args:
        session (AsyncSession): async session
        breed (str | None): cat's breed
        name (str | None): cat's name

    Returns:
        Cat: database objects (iterable). cat.name: str, cat.age: int, cat.color: str, cat.breed: str
    """

    # Get all cats from database OR with specific breed
    if name is None:
        if breed is None:
            cats = await session.scalars(select(Cat))
        else:
            cats = await session.scalars(select(Cat).where(Cat.breed == breed))

    # Get only one cat by it's name
    else:
        cats = await session.scalars(select(Cat).where(Cat.name == name))

    return cats.all()


async def get_breeds(session: AsyncSession) -> list[str]:
    """Get all breeds from database

    Args:
        session (AsyncSession): async session

    Returns:
        list[str]: list of breeds
    """

    breeds = await session.scalars(select(Cat.breed))
    return breeds.all()
