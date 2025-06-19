import asyncio
import datetime
from datetime import date

from fastapi import APIRouter, Query
from fastapi_cache.decorator import cache

from app.exceptions import InvalidDateRangeException
from app.hotels.dao import HotelDAO
from app.hotels.schemas import SHotel, SHotelOut

router = APIRouter(prefix='/hotels', tags=['Отели & Комнаты'])


@router.get('/{location}')
@cache(expire=40)
async def get_hotels_by_location_and_time(
        location: str,
        date_from: date = Query(..., description=f'Например {datetime.datetime.now().date()}'),
        date_to: date = Query(..., description=f'Например {datetime.datetime.now().date()}')
) -> list[SHotelOut]:
    if date_from > date_to:
        raise InvalidDateRangeException
    await asyncio.sleep(3)
    hotels = await HotelDAO.find_all(location, date_from, date_to)
    return hotels
