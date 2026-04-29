from src.api.dependecies import DBDep
from fastapi import APIRouter, HTTPException, Response, Body
from src.api.dependecies import UserIdDep
from src.schemas.users import UserRequestAdd, UserAdd
from src.services.auth import AuthService

router = APIRouter(prefix="/auth", tags=["authorization"])


@router.post("/register")
async def register_user(
        db: DBDep,
        user_data: UserRequestAdd = Body(),
):
    hashed_password = AuthService().hash_password(user_data.password)
    new_user_data = UserAdd(email=user_data.email, hashed_password=hashed_password)
    await db.users.add(new_user_data)
    await db.commit()
    return {"status": "OK"}

 
@router.post("/login")
async def login_user(
        db: DBDep,
        response: Response,
        user_data: UserRequestAdd = Body(),
):
    user = await db.users.get_user_with_hashed_password(email=user_data.email)
    if not user:
        raise HTTPException(status_code=401, detail="User is not exist")
    if not AuthService().verify_password(user_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Wrong password")
    access_token = AuthService().create_access_token({"user_id": user.id})
    response.set_cookie("access_token", access_token)
    return {"access_token": access_token}

@router.post("/logout")
async def logout(response: Response):
    response.delete_cookie("access_token")
    return {"status": "OK"}


@router.get("/only_auth")
async def only_auth(
        db: DBDep,
        user_id: UserIdDep
):
    user = await db.users.get_one_or_none(id=user_id)
    return user



