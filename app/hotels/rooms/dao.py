from datetime import date

from sqlalchemy import and_, func, select

from app.bookings.models import Bookings
from app.dao.base import BaseDAO
from app.database import async_session_maker
from app.hotels.rooms.models import Rooms


class RoomDAO(BaseDAO):
    model = Rooms

    @classmethod
    async def find_all(
        cls,
        hotel_id: int,
        date_from: date,
        date_to: date,
    ):
        async with async_session_maker() as session:
            booked_rooms = (
                select(
                    Bookings.room_id,
                    func.count(Bookings.room_id).label("booked_quantity"),
                )
                .where(
                    and_(Bookings.date_from <= date_to, Bookings.date_to >= date_from)
                )
                .group_by(Bookings.room_id)
            ).cte("booked_rooms")

            left_rooms = (
                select(
                    Rooms.__table__.columns,
                    (Rooms.price * (date_to - date_from).days).label("total_cost"),
                    (
                        Rooms.quantity
                        - func.coalesce(booked_rooms.c.booked_quantity, 0)
                    ).label("rooms_left"),
                )
                .join(booked_rooms, Rooms.id == booked_rooms.c.room_id, isouter=True)
                .where(Rooms.hotel_id == hotel_id)
            )
            rooms_left = await session.execute(left_rooms)
            print(rooms_left)
            return rooms_left.mappings().all()
