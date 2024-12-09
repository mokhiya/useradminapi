from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from app.core.database import SessionDep
from app.core.models.models import User
from app.core.security.user import get_current_active_user
from app.schemas.user import UserOut, UserBase, StandardResponse

router = APIRouter(
    tags=["users"]
)


@router.get("/users/me/", response_model=UserOut)
async def read_users_me(current_user: Annotated[User, Depends(get_current_active_user)]):
    return current_user


@router.put("/users/me/", response_model=UserOut)
async def update_my_profile(
    user_data: UserBase,
    current_user: Annotated[User, Depends(get_current_active_user)],
    session: SessionDep = Depends()
):
    for key, value in user_data.dict(exclude_unset=True).items():
        setattr(current_user, key, value)
    session.commit()
    session.refresh(current_user)
    return current_user


@router.post("/users/change/password", response_model=StandardResponse)
async def change_password(
        old_password: str,
        new_password: str,
        current_user: Annotated[User, Depends(get_current_active_user)],
        session: SessionDep = Depends()
):
    if current_user.password != old_password:
        raise HTTPException(status_code=400, detail="Old password is incorrect")

    current_user.password = new_password
    session.commit()
    session.refresh(current_user)
    return StandardResponse(success=True, message="Password updated successfully")
