from typing import Dict

from pydantic import BaseModel


class SHotel(BaseModel):
    id: int
    name: str
    location: str
    services: list
    rooms_quantity: int
    image_id: int

class SHotelOut(SHotel):
    rooms_left: int