import datetime
from datetime import date

from fastapi import APIRouter, Depends, status, Query

from app.bookings.dao import BookingDAO
from app.bookings.schemas import SBooking
from app.exceptions import RoomCannotBeBookedException, InvalidDateRangeException
from app.tasks.tasks import send_booking_confirmation_email
from app.users.dependencies import get_current_user
from app.users.models import Users

router = APIRouter(
    prefix='/bookings',
    tags=['Бронирования']
)


@router.get('')
async def get_bookings(
        user: Users = Depends(get_current_user)
) -> list[SBooking]:
    return await BookingDAO.find_all(user_id=user.id)


@router.post('')
async def add_booking(
        room_id: int,
        date_from: date = Query(..., description=f'Например {datetime.datetime.now().date()}'),
        date_to: date = Query(..., description=f'Например {datetime.datetime.now().date()}'),
        user: Users = Depends(get_current_user)
):
    if date_from > date_to:
        raise InvalidDateRangeException
    booking = await BookingDAO.add(user.id, room_id, date_from, date_to)
    if not booking:
        raise RoomCannotBeBookedException
    booking_dict = SBooking.model_validate(booking).model_dump()
    send_booking_confirmation_email.delay(booking_dict, user.email)
    return booking_dict


@router.delete('/{booking_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_booking(
        booking_id: int,
        user: Users = Depends(get_current_user)
) -> None:
    await BookingDAO.delete(id=booking_id)
