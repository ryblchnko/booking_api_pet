from typing import Optional

from pydantic import BaseModel


class SRoom(BaseModel):
    id: int
    hotel_id: int
    name: str
    description: str
    services: list
    price: int
    quantity: int
    image_id: Optional[int]


class SRoomOut(SRoom):
    total_cost: int = None
    rooms_left: int = None
