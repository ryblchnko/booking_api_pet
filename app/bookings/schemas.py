from datetime import date

from pydantic import BaseModel, ConfigDict
from pydantic_settings import SettingsConfigDict


class SBooking(BaseModel):
    id: int
    room_id: int
    user_id: int
    date_to: date
    date_from: date
    price: int
    total_cost: int
    total_days: int

    model_config = SettingsConfigDict(from_attributes=True)
