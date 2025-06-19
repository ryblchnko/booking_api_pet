from datetime import date

from pydantic import BaseModel

class SBookings(BaseModel):
    id: int
    room_id: int
    user_id: int
    date_to: date
    date_from: date
    price: int
    total_cost: int
    total_days: int
