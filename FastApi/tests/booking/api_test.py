import pytest
from sqlalchemy import delete

from src.models.bookings import BookingsOrm
from tests.conftest import get_db_null_pull


@pytest.mark.parametrize("room_id, date_from, date_to, status_code", [
    (1, "2025-04-11", "2025-04-16", 200),
    (1, "2025-03-11", "2025-04-09", 200),
    (1, "2025-04-11", "2025-04-16", 200),
    (1, "2024-02-11", "2024-03-09", 200),
    (1, "2024-02-11", "2024-03-09", 200),
    (1, "2024-02-11", "2024-03-09", 200),
    (1, "2024-02-11", "2024-03-09", 500),
])
async def test_booking_add(room_id, date_from, date_to, status_code, db, login_user):
    room_id = (await db.rooms.get_all())[0].id
    hotel_id = (await db.hotels.get_all())[0].id
    response = await login_user.post(
        "/bookings",
        json={
            "hotel_id": hotel_id,
            "room_id": room_id,
            "date_from": date_from,
            "date_to": date_to
        }
    )
    if status_code == 200:
        assert response.status_code == 200
        res = response.json()
        assert isinstance(res, dict)
        assert res["status"] == "OK"

@pytest.fixture(scope="module")
async def delete_table():
    async for _db in get_db_null_pull():
        await _db.bookings.remove()
        await _db.commit()

@pytest.mark.parametrize("room_id, date_from, date_to, count", [
(1, "2025-04-11", "2025-04-16", 1),
(1, "2025-04-11", "2025-04-16", 2)])
async def test_booking_add_and_check(delete_table, room_id, date_from, date_to, count, db, login_user):
    room_id = (await db.rooms.get_all())[0].id
    hotel_id = (await db.hotels.get_all())[0].id
    response = await login_user.post(
        "/bookings",
        json={
            "hotel_id": hotel_id,
            "room_id": room_id,
            "date_from": date_from,
            "date_to": date_to
        }
    )
    res = response.json()
    assert isinstance(res, dict)
    assert res["status"] == "OK"
    get_bookings = await login_user.get("/bookings/me")
    assert get_bookings.status_code == 200
    res = get_bookings.json()
    assert len(res) == count

