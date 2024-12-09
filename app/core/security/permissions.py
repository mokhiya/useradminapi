from typing import Annotated

from fastapi import Depends, HTTPException
from rest_framework import status

from app.core.models import User
from app.core.security.user import get_current_active_user


async def is_admin(user: Annotated[User, Depends(get_current_active_user)]) -> User:
    if user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not admin"
        )
    return user


async def is_user(user: Annotated[User, Depends(get_current_active_user)]) -> User:
    if user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not user"
        )
    return user


async def is_admin_or_user(user: Annotated[User, Depends(get_current_active_user)]) -> User:
    if user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are neither admin nor user"
        )
    return user