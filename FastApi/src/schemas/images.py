from pydantic import BaseModel

class AddImage(BaseModel):
    hotel_id: int

class Image(AddImage):
    id: int