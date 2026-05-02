from fastapi import HTTPException
from pydantic import BaseModel
from sqlalchemy import insert

from src.models.bookings import BookingsOrm
from src.repositories.base import BaseRepository
from src.repositories.mappers.mappers import BookingsDataMapper
from src.repositories.utils import room_ids_for_booking
from src.schemas.bookings import BookingAdd


class BookingsRepository(BaseRepository):
    model = BookingsOrm
    mapper = BookingsDataMapper

    async def add_booking(self, data: BookingAdd, hotel_id: int):
        rooms_ids_to_get = room_ids_for_booking(
            date_from=data.date_from,
            date_to=data.date_to,
            hotel_id=hotel_id
        )
        rooms_ids_to_book = await self.session.execute(rooms_ids_to_get)
        room_ids: list[int] = rooms_ids_to_book.scalars().all()
        if data.room_id in room_ids:
            new_booking = await self.add(data)
            return new_booking
        else:
            raise HTTPException(status_code=500, detail="Booking not found")





