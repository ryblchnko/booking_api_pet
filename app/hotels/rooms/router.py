import datetime
from datetime import date

from fastapi import APIRouter, Query

from app.exceptions import InvalidDateRangeException
from app.hotels.rooms.dao import RoomDAO
from app.hotels.rooms.schemas import SRoomOut

router = APIRouter(prefix='/hotels', tags=['Отели & Комнаты'])

@router.get('/{hotel_id}/rooms')
async def get_rooms_by_time(
        hotel_id: int,
        date_from: date = Query(..., description=f'Например {datetime.datetime.now().date()}'),
        date_to: date = Query(..., description=f'Например {datetime.datetime.now().date()}')
) -> list[SRoomOut]:
    rooms = await RoomDAO.find_all(hotel_id, date_from, date_to)
    return rooms