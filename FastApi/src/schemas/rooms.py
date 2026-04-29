from typing import Optional

from pydantic import BaseModel

from src.schemas.facilities import Facilities


class AddRoomsRequest(BaseModel):
    title: str
    description: str | None = None
    price: int
    quantity: int
    facilities_ids: list[int] = list

class AddRooms(BaseModel):
    hotel_id: int
    title: str
    description: str | None
    price: int
    quantity: int

class Rooms(AddRooms):
    id: int

class PatchRooms(BaseModel):
    hotel_id: int | Optional[int] = None
    title: str | Optional[str] = None
    description: str | Optional[str] = None
    price: int | Optional[int] = None
    quantity: int | Optional[int] = None
    facilities_ids: list[int] = list

class PatchRoomsRequest(BaseModel):
    title: str | Optional[str] = None
    description: str | Optional[str] = None
    price: int | Optional[int] = None
    quantity: int | Optional[int] = None
    facilities_ids: list[int] | None = None

class RoomsWithRels(Rooms):
    facilities: list[Facilities]