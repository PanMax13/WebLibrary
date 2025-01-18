import asyncio

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from os import getenv
from .models import Base

load_dotenv()

user = getenv("USER")
password = getenv("PASSWORD")
host = getenv("HOST")
port = getenv("PORT")
db = getenv("DB")

engine = create_async_engine(f'postgresql+asyncpg://{user}:{password}@{host}:{port}/{db}')

async_session = sessionmaker(
    bind=engine,
    class_=AsyncSession
)

async def connection():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        return "success"


async def createSession():
    async with async_session() as session:
        yield session
