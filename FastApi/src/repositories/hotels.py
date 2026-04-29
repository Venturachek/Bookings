from datetime import date

from sqlalchemy import func, select
from src.models.hotels import HotelsOrm
from src.models.rooms import RoomsOrm
from src.repositories.base import BaseRepository
from src.repositories.mappers.mappers import HotelsDataMapper
from src.repositories.utils import room_ids_for_booking
from src.schemas.hotels import Hotel


class HotelsRepository(BaseRepository):
    model = HotelsOrm
    mapper = HotelsDataMapper


    async def get_filtered_by_time(
            self,
            date_from: date,
            date_to: date,
            title: str | None = None,
            location: str | None = None,
            offset: int | None = None,
            limit: int | None = None
    ) -> list[Hotel]:
        rooms_ids_to_get = room_ids_for_booking(date_from=date_from, date_to=date_to)
        hotel_ids_to_get = (select(RoomsOrm.hotel_id)
                     .select_from(RoomsOrm)
                     .filter(RoomsOrm.id.in_(rooms_ids_to_get)))
        query = select(self.model).filter(HotelsOrm.id.in_(hotel_ids_to_get))
        if location:
            query = query.where(func.trim(HotelsOrm.location).ilike(f"%{location}%"))
        if title:
            query = query.where(func.trim(HotelsOrm.title).ilike(f"%{title}%"))
        query = (query
                 .limit(limit)
                 .offset(offset)
                 )
        result = await self.session.execute(query)

        return [self.mapper.map_to_domain(hotel) for hotel in result.scalars().all()]