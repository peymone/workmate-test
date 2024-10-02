# Third party libraries
from fastapi import FastAPI
import uvicorn

# BuildIn libraries
from os import getenv
import asyncio

# My modules
from routers import admin
from db.base import create_db


# API configuration
app = FastAPI()
app.include_router(admin.router)


def init_cats_db() -> None:
    """Create cats database if not exist. Default path is: {my_app_dir}/db/cats.db"""

    creation_result = asyncio.run(create_db())
    print(creation_result[1])  # print result message


if __name__ == '__main__':
    init_cats_db()
