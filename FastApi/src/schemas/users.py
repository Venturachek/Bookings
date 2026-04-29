from pydantic import BaseModel, ConfigDict, Field, EmailStr


class UserRequestAdd(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=72)

class UserAdd(BaseModel):
    email: EmailStr
    hashed_password: str

class User(BaseModel):
    id: int
    email: EmailStr

    model_config = ConfigDict(from_attributes=True)


class UserWithHashedPassword(User):
    hashed_password: str

