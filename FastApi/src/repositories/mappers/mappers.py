from src.models.bookings import BookingsOrm
from src.models.facilities import FacilitiesOrm, RoomsFacilitiesOrm
from src.models.hotels import HotelsOrm
from src.models.images import ImageOrm
from src.models.rooms import RoomsOrm
from src.models.user import UsersOrm
from src.repositories.mappers.base import DataMapper
from src.schemas.bookings import Booking
from src.schemas.facilities import RoomFacility, Facilities
from src.schemas.hotels import Hotel
from src.schemas.images import Image
from src.schemas.rooms import Rooms
from src.schemas.users import User


class HotelsDataMapper(DataMapper):
    model = HotelsOrm
    schema = Hotel

class BookingsDataMapper(DataMapper):
    model = BookingsOrm
    schema = Booking

class FacilitiesDataMapper(DataMapper):
    model = FacilitiesOrm
    schema = Facilities

class RoomFacilitiesDataMapper(DataMapper):
    model = RoomsFacilitiesOrm
    schema = RoomFacility

class UsersDataMapper(DataMapper):
    model = UsersOrm
    schema = User

class RoomsDataMapper(DataMapper):
    model = RoomsOrm
    schema = Rooms

class ImageDataMapper(DataMapper):
    model = ImageOrm
    schema = Image