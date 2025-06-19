import asyncio
import json

import pytest
from sqlalchemy import insert

from app.config import settings
from app.database import Base, async_session_maker, engine

from app.bookings.models import Bookings
from app.hotels.models import Hotels
from app.hotels.rooms.models import Rooms
from app.users.models import Users


@pytest.fixture(scope='session', autouse=True)
async def prepare_database():
    assert settings.MODE == 'TEST'

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    def open_mock_json(model: str):
        with open('app/tests/mock_{model}.json', 'r') as file:
            return json.load(file)

    hotels = open_mock_json('hotels')
    bookings = open_mock_json('bookings')
    rooms = open_mock_json('rooms')
    users = open_mock_json('users')

    async with async_session_maker() as session:
        add_hotels = insert(Hotels).values(hotels)
        add_rooms = insert(Rooms).values(rooms)
        add_bookings = insert(Bookings).values(bookings)
        add_users = insert(Users).values(users)

    await session.execute(add_hotels)
    await session.execute(add_rooms)
    await session.execute(add_bookings)
    await session.execute(add_users)

    await session.commit()

@pytest.fixture(scope='session')
def event_loop(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()