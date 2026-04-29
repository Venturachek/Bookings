from datetime import date
from sqlalchemy import select
from sqlalchemy.orm import  joinedload
from src.models.rooms import RoomsOrm
from src.repositories.base import BaseRepository
from src.repositories.mappers.mappers import RoomsDataMapper
from src.repositories.utils import room_ids_for_booking
from src.schemas.rooms import  RoomsWithRels


class RoomsRepository(BaseRepository):
    model = RoomsOrm
    mapper = RoomsDataMapper

    async def get_filtered_by_time(self, date_from: date, date_to: date, hotel_id: int):
        room_ids = room_ids_for_booking(date_from=date_from, date_to=date_to, hotel_id=hotel_id)

        query = select(self.model).options(joinedload(self.model.facilities)).filter(RoomsOrm.id.in_(room_ids))

        result = await self.session.execute(query)
        return [RoomsWithRels.model_validate(model, from_attributes=True) for model in result.unique().scalars().all()]

    async def get_one_or_none_with_facilities(self, **filter_by):
        query = (
            select(self.model)
            .filter_by(**filter_by)
            .options(joinedload(self.model.facilities))
        )
        result = await self.session.execute(query)

        model = result.unique().scalars().one_or_none()

        if model is None:
            return None

        return self.mapper.map_to_domain(model)