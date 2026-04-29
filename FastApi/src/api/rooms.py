from fastapi import APIRouter, Body, Query
from fastapi_cache.decorator import cache
from src.api.dependecies import DBDep
from src.schemas.facilities import RoomFacilityAdd
from src.schemas.rooms import AddRooms, PatchRooms, AddRoomsRequest, PatchRoomsRequest
from datetime import date
router = APIRouter(prefix="/hotels", tags=["Rooms"])


@router.post("/{hotel_id}/rooms")
async def create_room(
        db: DBDep,
        hotel_id: int,
        rooms_data: AddRoomsRequest = Body()
):
    _room_data = AddRooms(hotel_id=hotel_id, **rooms_data.model_dump())

    data = await db.rooms.add(_room_data)
    facility_data = [RoomFacilityAdd(room_id=data.id, facility_id=f_id) for f_id in rooms_data.facilities_ids]
    await db.rooms_facilities.add_bulk(facility_data)
    await db.commit()
    return {"status": "OK", "data": data}


@router.put("/{hotel_id}/rooms/{room_id}")
async def update_rooms(
        db: DBDep,
        hotel_id: int,
        room_id: int,
        rooms_data: AddRoomsRequest
):
    _room_data = AddRooms(hotel_id=hotel_id, **rooms_data.model_dump())
    await db.rooms.edit(
        _room_data,
        id=room_id,
        hotel_id=hotel_id
    )
    await db.rooms_facilities.set_room_facilities(room_id, facilities_ids=rooms_data.facilities_ids)
    await db.commit()
    return {"status": "OK"}


@router.get("/{hotel_id}/rooms/{room_id}")
@cache(expire=20)
async def get_rooms(
        db: DBDep,
        hotel_id: int,
        room_id: int
):
    return await db.rooms.get_one_or_none_with_facilities(
        hotel_id=hotel_id,
        id=room_id
    )


@router.patch("/{hotel_id}/rooms/{room_id}")
async def patch_rooms(
        db: DBDep,
        hotel_id: int,
        room_id: int,
        rooms_data: PatchRoomsRequest
):
    _rooms_data_dict = rooms_data.model_dump(exclude_none=True)
    _room_data = PatchRooms(hotel_id=hotel_id, **_rooms_data_dict)
    if "facilities_ids" in _rooms_data_dict:
        db.rooms_facilities.set_room_facilities(room_id, facilities_ids=_rooms_data_dict["facilities_ids"])
    await db.rooms.partial_edit(
        _room_data,
        exclude_unset=True,
        id=room_id,
        hotel_id=hotel_id
        )
    await db.commit()
    return {"status": "OK"}


@router.delete("/{hotel_id}/rooms/{room_id}")
async def delete_rooms(
        db: DBDep,
        hotel_id: int,
        room_id: int
):
    await db.rooms.remove(
        hotel_id=hotel_id,
        id=room_id
        )
    await db.commit()
    return {"status": "OK"}

@router.get("/{hotel_id}/rooms")
@cache(expire=20)
async def get_rooms(
        db: DBDep,
        hotel_id: int,
        date_from: date = Query(example='2026-04-01'),
        date_to: date = Query(example='2026-04-09')
):
    return await db.rooms.get_filtered_by_time(hotel_id=hotel_id, date_from=date_from, date_to=date_to)

