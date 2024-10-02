# Third party libraries
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select
import pytest

# My modules
from db.base import Cat
from db.crud import add_cat, update_cat, delete_cat, get_cats, get_breeds


cats_good = [
    ('dick', 2, 'grey', 'british'),
    ('rita', 5, 'black', 'unknown'),
    ('vasya', 1, 'white', 'unknown'),
    ('temofei', 3, 'white-black', 'sibirian'),
    ('radja', 2, 'pink', 'sfinx')
]


cats_duplicate = [
    ('blackey', 5, 'black', 'scotland'),
    ('blackey', 5, 'black', 'scotland'),
]


@pytest.mark.asyncio()
async def test_add_cat_good_data(session):

    # Add cats to database
    for cat_data in cats_good:
        await add_cat(session, *cat_data)
        await session.commit()

    # Get cats from database and convert to list
    add_res = await session.scalars(select(Cat))
    cats = [(cat.name, cat.age, cat.color, cat.breed) for cat in add_res]

    # Check if cats present in database
    assert len(cats) == len(cats_good), "Not enough cats in database, must be 5"
    for cat_id_db, cat_from_sourse in zip(cats, cats_good):
        assert cat_id_db[0] == cat_from_sourse[0], "Wrong cat in database"


@pytest.mark.asyncio()
async def test_add_cat_duplicate_name(session):
    # Cat name must be unique
    for cat_data in cats_duplicate:
        await add_cat(session, *cat_data)

    with pytest.raises(IntegrityError):
        await session.commit()


@pytest.mark.asyncio()
async def test_update_cat_dont_exist_name(session):
    upd_res = await update_cat(session, 'dont_exist', 'new_name', 2, 'black', 'siberia')
    await session.commit()
    assert upd_res == None


@pytest.mark.asyncio()
async def test_update_cat_exist_name(session):
    # Add new cat to database
    await add_cat(session, name='mrcat', age=1, color='grey', breed='sfinx')
    await session.commit()

    # Update cat
    new_cat = ('good_cat', 2, 'black', 'siberia')
    upd_res = await update_cat(session, 'mrcat', *new_cat)

    # Get cats from database and convert to list
    add_res = await session.scalars(select(Cat))
    cats = [(cat.name, cat.age, cat.color, cat.breed) for cat in add_res]

    # Tests
    assert upd_res == None
    assert cats[0] == new_cat, "Old cat in database, alert!"


@pytest.mark.asyncio()
async def test_delete_cat(session):
    # Add new cat to database
    await add_cat(session, name='mrcat', age=1, color='grey', breed='sfinx')
    await session.commit()

    # Delete non-existent cat from database
    dont_exist_res = await delete_cat(session, 'dont_exist')
    assert dont_exist_res == None

    # Delete existing cat from database
    exist_res = await delete_cat(session, 'dont_exist')
    assert exist_res == None


@pytest.mark.asyncio()
async def test_get_cats_all_empty_db(session):
    # Get all cats from empy database
    res = await get_cats(session, breed=None, name=None)
    assert len(res) == 0, "Empty database have elements? Miracle"


@pytest.mark.asyncio()
async def test_get_cats_all_full_db(session):
    # Add cats to database
    for cat_data in cats_good:
        await add_cat(session, *cat_data)
        await session.commit()

    # Get cats from database, check len
    get_res = await get_cats(session, breed=None, name=None)
    cats_in_db = [(cat.name, cat.age, cat.color, cat.breed) for cat in get_res]
    assert len(cats_in_db) == len(cats_good), "Number of cats in db and in source is different"


@pytest.mark.asyncio()
async def test_get_cats_breeds_full_db(session):
    # Add cats to database
    for cat_data in cats_good:
        await add_cat(session, *cat_data)
        await session.commit()

    # Get cats from database, check len
    get_res = await get_cats(session, breed='unknown', name=None)
    cats_in_db = [(cat.name, cat.age, cat.color, cat.breed) for cat in get_res]
    assert len(cats_in_db) == len([cat for cat in cats_good if cat[-1] == 'unknown']
                                  ), "Number of cats with unknown breed in db and in source is different. Be vigalent!"


@pytest.mark.asyncio()
async def test_get_cats_one_full_db(session):
    # Add cats to database
    for cat_data in cats_good:
        await add_cat(session, *cat_data)
        await session.commit()

    # Get cats from database
    get_res = await get_cats(session, breed=None, name='temofei')
    cats_in_db = [(cat.name, cat.age, cat.color, cat.breed) for cat in get_res]

    # Check cats in db - must be 1
    assert len(cats_in_db) == 1, "Number of cats with name temodei in db and in source is different. Clones?"

    # Check if cat in database is right
    assert cats_in_db[0] == [cat for cat in cats_good if cat[0] ==
                             'temofei'][0], "Unknown cat in database woth name: temofei"


@pytest.mark.asyncio()
async def test_get_breeds_empty_db(session):
    result = await get_breeds(session)
    assert len(result) == 0, "Empty database have elements? Miracle"


@pytest.mark.asyncio()
async def test_get_breeds_full_db(session):
    # Add cats to database
    for cat_data in cats_good:
        await add_cat(session, *cat_data)
        await session.commit()

    result = await get_breeds(session)
    assert len(result) == len([cat[-1] for cat in cats_good])
