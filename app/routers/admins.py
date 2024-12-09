from typing import Annotated, List

from fastapi import APIRouter, Depends, HTTPException, Query

from app.core.database import SessionDep
from app.core.models.models import User
from app.schemas.user import UserOut, StandardResponse, UserBase

router = APIRouter(
    tags=["admins"]
)


@router.get("/users/", response_model=List[UserOut])
async def get_all_users(skip: int = Query(0, ge=0), limit: int = Query(10, ge=1), session: SessionDep = Depends()):
    users = session.query(User).offset(skip).limit(limit).all()
    return users


@router.get("/users/{user_id}/", response_model=UserOut)
async def get_user_by_id(user_id: int, session: SessionDep):
    user = session.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.put("/users/{user_id}/", response_model=UserOut)
async def update_user(user_id: int, user_data: UserBase, session: SessionDep):
    user = session.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    for key, value in user_data.dict(exclude_unset=True).items():
        setattr(user, key, value)
    session.commit()
    session.refresh(user)
    return user


@router.delete("/users/{user_id}", response_model=StandardResponse)
async def delete_user(user_id: int, session: SessionDep):
    user = session.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    session.delete(user)
    session.commit()
    return StandardResponse(success=True, message="User deleted successfully")
