from fastapi import APIRouter, Body

from src.api.dependecies import DBDep, UserIdDep
from src.schemas.bookings import BookingAddRequest, BookingAdd, Booking

router = APIRouter(prefix="/bookings", tags=["Booking"])

@router.post("")
async def add_booking(db: DBDep, user: UserIdDep, booking_data: BookingAddRequest = Body()):
    room = await db.rooms.get_one_or_none(id=booking_data.room_id)
    price: int = room.price
    _booking_data = BookingAdd(
        user_id=user,
        price=price,
        **booking_data.model_dump()
    )
    booking = await db.bookings.add_booking(_booking_data, hotel_id=booking_data.hotel_id)
    await db.commit()
    return {"status": "OK", "booking": booking}

@router.get("")
async def get_bookings(db: DBDep):
    return await db.bookings.get_all()


@router.get("/me")
async def get_bookings(db: DBDep, user: UserIdDep):
    return await db.bookings.get_filtered(user_id=user)