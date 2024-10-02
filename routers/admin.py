# Third party libraries
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import HTMLResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

# My modules
from routers.models import *
from db.base import get_session
from db.crud import add_cat as add_cat_db
from db.crud import get_cats as get_cats_db
from db.crud import get_breeds as get_breeds_db
from db.crud import update_cat as update_cat_db
from db.crud import delete_cat as delete_cat_db


# Router configuration
router = APIRouter(prefix='/admin', tags=['admin'])


# Path functions

@router.get('/', response_class=HTMLResponse)
async def index():
    return """
    <html>
        <head>
            <title>admin panel</title>
        </head>
        <body>
            <h1>Hello, admin</h1>
            <h2>Be ready to create some kittens</h2>
        </body>
    </html>
    """


@router.post('/cat', status_code=status.HTTP_201_CREATED)
async def add_cat(cat: AddCat, session: AsyncSession = Depends(get_session)) -> AddCatSucess:
    """Add new cat to database

    Args:
        cat (AddCat): name: str, age: int, color: str, breed: str
        session (AsyncSession, optional): sqlalchemy async session

    Raises:
        HTTPException: HTTP_500_INTERNAL_SERVER_ERROR when transaction failed

    Returns:
        AddCatSucess: message: str = "New cat successfully added to database"
    """

    await add_cat_db(session, cat.name, cat.age, cat.color, cat.breed)

    try:
        await session.commit()
        return AddCatSucess

    except IntegrityError as error:
        await session.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Transaction failed while adding new cat")


@router.patch('/cat')
async def update_cat(old_name: str, cat: AddCat, session: AsyncSession = Depends(get_session)) -> UpdateCatSucess:
    """Update cat data by passing cat's name

    Args:
        old_name (str): cat's old name
        cat (AddCat): new cat's data
        session (AsyncSession, optional): sqlalchemy async session

    Raises:
        HTTPException: HTTP_500_INTERNAL_SERVER_ERROR when transaction failed

    Returns:
        UpdateCatSucess: message: str = "Cat successfully updated"
    """

    await update_cat_db(session, old_name, cat.name, cat.age, cat.color, cat.breed)

    try:
        await session.commit()
        return UpdateCatSucess

    except Exception as error:
        await session.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Transaction failed while updating cat")


@router.delete('/cat')
async def delete_cat(name: str, session: AsyncSession = Depends(get_session)) -> DeleteCatSucess:
    """Delete cat by cat's name

    Args:
        name (str): cat's name
        session (AsyncSession, optional): sqlalchemy async session

    Raises:
        HTTPException: HTTP_500_INTERNAL_SERVER_ERROR when transaction failed

    Returns:
        DeleteCatSucess: message: str = "Cat successfully deleted"
    """

    await delete_cat_db(session, name)

    try:
        await session.commit()
        return DeleteCatSucess

    except Exception as error:
        await session.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Transaction failed while deleting cat")


@router.get('/cat')
async def get_cats(name: str = None, breed: str = None, session: AsyncSession = Depends(get_session)) -> list[AddCat]:
    """Get all cats from database OR with specific breed OR only one cat with specific name

    Args:
        breed (str) = None: specific breed (can be omitted)
        session (AsyncSession, optional): sqlalchemy async session

    Returns:
        list[AddCat]: list of name: str, age: int, color: str, breed: str
    """

    cats = await get_cats_db(session, breed, name)
    return [AddCat(name=cat.name, age=cat.age, color=cat.color, breed=cat.breed) for cat in cats]


@router.get('/breeds')
async def get_breeds(session: AsyncSession = Depends(get_session)) -> list[str]:
    """Get all breeds present in database

    Args:
        session (AsyncSession, optional): sqlalchemy async session

    Returns:
        list[str]: list of breeds
    """

    breeds = await get_breeds_db(session)
    return breeds
