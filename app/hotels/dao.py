from datetime import date

from sqlalchemy import func, select, and_

from app.bookings.models import Bookings
from app.dao.base import BaseDAO
from app.database import async_session_maker
from app.hotels.models import Hotels
from app.hotels.rooms.models import Rooms


class HotelDAO(BaseDAO):
    model = Hotels

    @classmethod
    async def find_all(
            cls,
            location: str,
            date_from: date,
            date_to: date
    ):
        async with async_session_maker() as session:
            booked_rooms = (
                select(
                    Rooms.hotel_id,
                    func.count(Bookings.id).label("booked_count")
                )
                .join(Rooms, Bookings.room_id == Rooms.id)
                .where(
                    and_(
                        Bookings.date_from <= date_to,
                        Bookings.date_to >= date_from
                    )
                )
                .group_by(Rooms.hotel_id)
            ).cte('booked_rooms')

            total_rooms = (
                select(
                    Rooms.hotel_id,
                    func.sum(Rooms.quantity).label("total_rooms")
                )
                .group_by(Rooms.hotel_id)
            ).cte('total_rooms')

            query = (
                select(
                    Hotels.__table__.columns,
                    (func.coalesce(total_rooms.c.total_rooms, 0) -
                     func.coalesce(booked_rooms.c.booked_count, 0)).label("rooms_left")
                )
                .join(
                    total_rooms,
                    total_rooms.c.hotel_id == Hotels.id,
                    isouter=True
                )
                .join(
                    booked_rooms,
                    booked_rooms.c.hotel_id == Hotels.id,
                    isouter=True
                )
                .where(
                    and_(
                        Hotels.location.like(f"%{location}%"),
                        (func.coalesce(total_rooms.c.total_rooms, 0) - func.coalesce(booked_rooms.c.booked_count, 0)) > 0
                    )
                )
            )

            result = await session.execute(query)
            return result.mappings().all()

