from passlib.context import CryptContext

from app.core.database import SessionDep
from app.core.models import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def validate_password(password: str, confirm_password: str) -> bool:
    if password != confirm_password:
        return False
    return True


def get_user_by_username(username: str, session: SessionDep) -> None | User:
    return session.query(User).filter(User.username == username).first()


def get_user_by_email(email: str, session: SessionDep) -> None | User:
    return session.query(User).filter(User.email == email).first()


def authenticate_user(username: str, password: str, session: SessionDep):
    user = get_user_by_username(username=username, session=session)
    if not user:
        return False
    if not verify_password(plain_password=password, hashed_password=user.password):
        return False
    return user
