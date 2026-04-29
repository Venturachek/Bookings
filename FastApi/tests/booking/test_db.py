from datetime import date

from src.schemas.bookings import BookingAdd


async def test_booking_crud(db):
    user = (await db.users.get_all())[0].id
    room_id = (await db.rooms.get_all())[0].id
    data = BookingAdd(
        user_id=user,
        room_id=room_id,
        date_from=date(2025, 4, 10),
        date_to=date(2025, 4, 15),
        price=100,
    )
    new_booking = await db.bookings.add(data)
    booking = await db.bookings.get_one_or_none(id=new_booking.id)
    assert booking
    assert booking.id == new_booking.id
    assert booking.user_id == new_booking.user_id
    assert booking.room_id == new_booking.room_id
    data_edit = BookingAdd(
        user_id=user,
        room_id=room_id,
        date_from=date(2025, 4, 11),
        date_to=date(2025, 4, 16),
        price=110,
    )
    await db.bookings.edit(id=new_booking.id, data=data_edit)
    updated_booking = await db.bookings.get_one_or_none(id=new_booking.id)
    assert updated_booking
    assert updated_booking.id == new_booking.id
    assert updated_booking.user_id == new_booking.user_id

    await db.bookings.remove(id=new_booking.id)
    booking = await db.bookings.get_one_or_none(id=new_booking.id)
    assert booking is None
    await db.commit()
