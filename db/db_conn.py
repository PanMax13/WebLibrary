import asyncio

from sqlalchemy.ext.asyncio import create_async_engine
from dotenv import load_dotenv
from os import getenv
from models import Base

load_dotenv('../.env')

user = getenv("USER")
password = getenv("PASSWORD")
host = getenv("HOST")
port = getenv("PORT")
db = getenv("DB")

print(f"user={user}, password={password}, host={host}, port={port}, db={db}")
engine = create_async_engine(f'postgresql+asyncpg://{user}:{password}@{host}:{port}/{db}')

async def connection():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
        return "success"

print(asyncio.run(connection()))