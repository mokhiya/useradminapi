from datetime import timedelta, datetime

import jwt

from app.core.config import SECRET_KEY, ALGORITHM

# openssl rand -hex 32
ACCESS_TOKEN_EXPIRE_MINUTES = 1440


def create_access_token(data: dict, expire_delta: timedelta = None):
    to_encode = data.copy()
    if expire_delta:
        expire = datetime.utcnow() + expire_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    access_token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return access_token
