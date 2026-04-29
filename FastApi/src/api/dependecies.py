
from fastapi import Depends, Query, Request, HTTPException
from pydantic import BaseModel
from typing import Annotated

from src.database import async_session_maker
from src.services.auth import AuthService
from src.utils.dbmanager import DBManager

# Pagination
class PaginationParams(BaseModel):
    page: Annotated[int | None, Query(1, ge=1)]
    per_page: Annotated[int | None, Query(None, ge=1, lt=30)]


PaginationDep = Annotated[PaginationParams, Depends()]

# users dep
def get_token(request: Request):
    access_token = request.cookies.get("access_token", None)
    if not access_token:
        raise HTTPException(status_code=401, detail="There is no token")
    return access_token


def get_current_user_id(token: str = Depends(get_token)) -> int:
    data = AuthService().encode_token(token)
    return data["user_id"]


UserIdDep = Annotated[int, Depends(get_current_user_id)]


# context manager
async def get_db():
    async with DBManager(session_factory=async_session_maker) as db:
        yield db

DBDep = Annotated[DBManager, Depends(get_db)]