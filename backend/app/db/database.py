from sqlmodel import SQLModel, create_engine, Session
from typing import Generator
from app.core.config import get_settings

settings = get_settings()

engine = create_engine(settings.DATABASE_URL, connect_args={"check_same_thread": False})

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session