
from src.schemas.hotels import HotelAdd

async def test_add_hotel(db):
    data = HotelAdd(title="MEGA hotel", location="Dubai")
    await db.hotels.add(data)
    await db.commit()












