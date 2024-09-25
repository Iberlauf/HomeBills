"""Models module."""

from enum import Enum
from datetime import date
from decimal import Decimal
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


class Address(AddressBase, table=True):
    """Adress create model."""

    id: int | None = Field(default=None, primary_key=True)
    users: list["User"] = Relationship(back_populates="address")
    businesses: list["Business"] = Relationship(back_populates="address")


class UserBase(SQLModel):
    """User base model."""

    first_name: str
    last_name: str
    email: EmailStr | None


class User(UserBase, table=True):
    """User create model."""

    id: int | None = Field(default=None, primary_key=True)
    address_id: int = Field(default=None, foreign_key="address.id")
    address: Address = Relationship(back_populates="users")


class BusinessBase(SQLModel):
    """Business base model."""

    name: str
    contact_email: EmailStr | None
    bank_account: int
    pdf_producer: str
    type: BusinessType


class Business(BusinessBase, table=True):
    """Business create model."""

    id: int | None = Field(default=None, primary_key=True)
    address_id: int = Field(default=None, foreign_key="address.id")
    address: Address = Relationship(back_populates="businesses")
    bills: list["Bill"] = Relationship(back_populates="business")


class BillBase(SQLModel):
    """Bill base model."""

    name: str
    payed: bool = Field(default=False)
    date_payed: date = Field(default=date.today())
    ammount: Decimal = Field(default=0, decimal_places=2)


class Bill(BillBase, table=True):
    """Bill create model."""

    id: int | None = Field(default=None, primary_key=True)
    business_id: int = Field(default=None, foreign_key="business.id")
    business: Business = Relationship(back_populates="bills")
