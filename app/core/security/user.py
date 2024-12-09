from typing import Annotated

import jwt
from fastapi import Depends, HTTPException, status
from jwt import InvalidTokenError

from app.core.config import SECRET_KEY, ALGORITHM
from app.core.database import SessionDep
from app.core.models import User
from app.core.security.auth import get_user_by_username
from app.routers.auth import oauth2_scheme
from app.schemas.user import TokenPayload

# openssl rand -hex 32
ACCESS_TOKEN_EXPIRE_MINUTES = 1440


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], session: SessionDep):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_payload = TokenPayload(username=username)
    except InvalidTokenError:
        raise credentials_exception
    user = get_user_by_username(username=token_payload.username, session=session)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(
        current_user: Annotated[User, Depends(get_current_user)],
):
    if current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
