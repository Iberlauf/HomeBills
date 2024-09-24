"""Database module."""

from sqlmodel import SQLModel, create_engine
from sqlalchemy import Engine


db_name: str = "database.db"
db_url: str = f"sqlite:///{db_name}"

engine: Engine = create_engine(url=db_url, echo=True)


def create_db_and_tables() -> None:
    """Function that creates a database instance and tables."""
    SQLModel.metadata.create_all(bind=engine)
