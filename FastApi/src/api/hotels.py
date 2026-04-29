from fastapi import Query, APIRouter, Body
from datetime import date
from fastapi_cache.decorator import cache
from src.schemas.hotels import  HotelPATCH, HotelAdd
from src.api.dependecies import PaginationDep, DBDep
router = APIRouter(prefix="/hotel", tags=["Hotels"])




@router.get("")
@cache(expire=20)
async def get_hotels(
        db: DBDep,
        pag: PaginationDep,
        location: str | None = Query(None, description="location"),
        title: str | None = Query(None, description="Hotel`s name"),
        date_from: date = Query(example='2026-04-01'),
        date_to: date = Query(example='2026-04-09')

):
    per_page = pag.per_page or 5
    return await db.hotels.get_filtered_by_time(
            date_from=date_from,
            date_to=date_to,
            title=title,
            location=location,
            limit=per_page,
            offset=per_page * (pag.page - 1)
        )


@router.get("/{hotel_id}")
@cache(expire=20)
async def get_hotel_by_id(hotel_id: int, db: DBDep):
        return await db.hotels.get_one_or_none(
            id=hotel_id
        )


@router.post("")
async def create_hotel(db: DBDep, hotel_data: HotelAdd = Body(openapi_examples={
    "1": {"summary": "Sochi", "value": {
        "title": "Hotel Sochi 5 stars",
        "location": "Sea street 2"
    }},
    "2": {"summary": "Dubai", "value": {
        "title": "Dubai best Hotel",
        "location": "Dubaimall street 1"
    }}
})
):
    await db.hotels.add(hotel_data)
    await db.commit()
    return{"status": "OK"}


@router.put("/{hotel_id}")
async def update_hotel(db: DBDep, hotel_id: int, hotel_data: HotelAdd, ):
    db.hotels.edit(
        id=hotel_id,
        data=hotel_data
        )
    await db.commit()
    return {"status": "OK"}


@router.patch("/{hotel_id}", summary="Partial update of hotel data",
              description="Here you can update [title] or [name]")
async def patch_hotel(db: DBDep, hotel_id: int, hotel_data: HotelPATCH):
    await db.hotels.edit(
        id=hotel_id,
        data=hotel_data,
        exclude_unset=True
    )
    await db.commit()
    return {"status": "OK"}
@router.delete("/{hotel_id}")
async def delete_hotel(db: DBDep, hotel_id: int):
    await db.hotels.remove(
        id=hotel_id
        )
    await db.commit()
    return {"status": "OK"}


