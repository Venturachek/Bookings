from src.database import Base
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import  ForeignKey

class ImageOrm(Base):
    __tablename__ = 'images'

    id: Mapped[int] = mapped_column(primary_key=True)
    hotel_id: Mapped[int] = mapped_column(ForeignKey('hotels.id'))

