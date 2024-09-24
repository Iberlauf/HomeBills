"""Models module."""

from enum import Enum
from pydantic import EmailStr
from sqlmodel import Field, Relationship, SQLModel


class BusinessType(str, Enum):
    """Type enum."""

    ELECTRICAL = "electrical"
    WATER = "water"
    CABLE = "cable"
    CLEANING = "cleaning"
    PHONE = "phone"
    TAX = "tax"
    HEATING = "heating"
    GARBAGE = "garbage"


class AddressBase(SQLModel):
    """Adress base model."""

    street: str
    number: str
    city: str
    postal_code: int


class AddressCreate(AddressBase, table=True):
    """Adress create model."""

    id: int | None = Field(default=None, primary_key=True)
    users: list["UserBase"] = Relationship(back_populates="address")
    businesses: list["BusinessBase"] = Relationship(back_populates="address")


class UserBase(SQLModel):
    """User base model."""

    first_name: str
    last_name: str
    email: EmailStr


class UserCreate(UserBase, table=True):
    """User create model."""

    id: int | None = Field(default=None, primary_key=True)
    address_id: int = Field(default=None, foreign_key="addresscreate.id")
    address: AddressCreate = Relationship(back_populates="users")


class BusinessBase(SQLModel):
    """Business base model."""

    name: str
    contact_email: EmailStr
    bank_account: int
    pdf_producer: str
    type: BusinessType


class BusinessCreate(BusinessBase, table=True):
    """Business create model."""

    id: int | None = Field(default=None, primary_key=True)
    address_id: int = Field(default=None, foreign_key="addresscreate.id")
    address: AddressCreate = Relationship(back_populates="businesses")
