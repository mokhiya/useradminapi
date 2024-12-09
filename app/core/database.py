from typing import Annotated

from fastapi import Depends
from sqlmodel import Session, create_engine
from app.core.config import DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME

# sqlite_name = "database.db"
# database_url = f"sqlite:///{sqlite_name}"
database_url = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"


# connect_args = {"check_same_thread": False}
engine = create_engine(database_url)


# connecting to database
def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]
