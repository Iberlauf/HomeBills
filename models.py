"""Models module."""

from sqlmodel import SQLModel, Field


class AdressBase(SQLModel):
    """Adress base model."""

    street: str
    number: str
    city: str
    postal_code: int


class AdressCreate(AdressBase, table=True):
    """Adress create model."""

    id: int = Field(default=None, primary_key=True)
