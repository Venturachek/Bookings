import asyncio
from unittest import mock
from fastapi_cache import FastAPICache
from fastapi_cache.backends.inmemory import InMemoryBackend
from httpx import AsyncClient, ASGITransport
from pytest import fixture
import pytest
import json

from src.api.dependecies import get_db
from src.config import settings
from src.main import app
from src.models import *
from src.database import Base, engine_null_pull, async_session_maker_null_pull
from src.schemas.hotels import HotelAdd
from src.schemas.rooms import AddRooms
from src.utils.dbmanager import DBManager



@pytest.fixture(scope="function")
async def db() -> DBManager:
    async for db in get_db_null_pull():
        yield db


async def get_db_null_pull():
    async with DBManager(session_factory=async_session_maker_null_pull) as db:
        yield db

app.dependency_overrides[get_db] = get_db_null_pull


@pytest.fixture(scope="session", autouse=True)
async def async_main():
    assert settings.MODE == "TEST"
    FastAPICache.init(InMemoryBackend())
    async with engine_null_pull.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


    with open("tests/mock_hotels.json") as file_hotels:
        hotels = json.load(file_hotels)
    with open("tests/mock_rooms.json") as file_rooms:
        rooms = json.load(file_rooms)
    rooms = [AddRooms.model_validate(room) for room in rooms]
    hotels = [HotelAdd.model_validate(hotel) for hotel in hotels]
    async with DBManager(session_factory=async_session_maker_null_pull) as _db:
        await _db.hotels.add_bulk(hotels)
        await _db.rooms.add_bulk(rooms)
        await _db.commit()



@pytest.fixture(scope="session")
async def ac() -> AsyncClient:
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac

@pytest.fixture(scope="session", autouse=True)
async def add_user(ac, async_main):
    await ac.post(
            "/auth/register",
                json={"email": "email123@gmail.com",
                      "password": "qwerty1234"}
        )

