from fastapi import Query, APIRouter, Body

from fastapi_cache.decorator import cache

from src.api.dependecies import DBDep
from src.schemas.facilities import FacilitiesAdd

router = APIRouter(prefix="/facilities", tags=["Facilities"])

@router.post("")
async def new_facility(db : DBDep, fac_data: FacilitiesAdd = Body()):
    facility = await db.facilities.add(fac_data)
    await db.commit()
    return {"status": "OK", 'facility': facility}

@router.get("")
@cache(expire=20)
async def get_facilities(db: DBDep):
    return await db.facilities.get_all()


@router.delete("/{facility_id}")
async def del_facility(db: DBDep, facility_id: int):
    await db.facilities.remove(
        id=facility_id
    )
    await db.commit()
    return {"status": "OK"}