from src.models.images import ImageOrm
from src.repositories.base import BaseRepository
from src.repositories.mappers.mappers import ImageDataMapper


class ImageRepository(BaseRepository):
    model: ImageOrm
    mapper =  ImageDataMapper