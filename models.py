"""Models module."""

from datetime import date
from decimal import Decimal
from enum import Enum

from pydantic import EmailStr, HttpUrl, field_validator
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

    @field_validator("postal_code")
    @classmethod
    def validate_postal_code(cls, value: int) -> int:
        """
        Validate that the postal code is a 5-digit integer.

        Args:
            value (int): The postal code to validate.

        Returns:
            int: The validated postal code if it meets the requirements.

        Raises:
            ValueError: If the postal code is not a 5-digit number.
        """
        if value < 10000 or value > 99999:
            raise ValueError("Postal code must be a 5-digit number")
        return value


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
    bank_account: int
    pdf_producer: str
    type: BusinessType
    url: HttpUrl

    @field_validator("bank_account")
    @classmethod
    def validate_account_number(cls, value: int) -> int:
        """
        Validate that the bank account number is exactly 18 digits.

        Args:
            v (int): The bank account number to validate.

        Returns:
            int: The validated bank account number if it meets the requirements.

        Raises:
            ValueError: If the bank account number is not 18 digits long.
        """
        if value < 10**17 or value > 10**18 - 1:
            raise ValueError("Bank account number must be exactly 18 digits")
        return value

    @field_validator("url")
    @classmethod
    def validate_http_url(cls, value: HttpUrl) -> HttpUrl:
        """
        Validate that the URL starts with 'http' or 'https'.

        Args:
            value (HttpUrl): The URL to validate.

        Returns:
            HttpUrl: The validated URL if it meets the requirements.

        Raises:
            ValueError: If the URL does not start with 'http' or 'https'.
        """
        if value.scheme not in ["http", "https"]:
            raise ValueError("URL must start with 'http' or 'https'")
        return value


class Business(BusinessBase, table=True):
    """Business create model."""

    id: int | None = Field(default=None, primary_key=True)
    address_id: int = Field(default=None, foreign_key="address.id")
    address: Address = Relationship(back_populates="businesses")
    bills: list["Bill"] = Relationship(back_populates="business")


class BillBase(SQLModel):
    """Bill base model."""

    name: str
    date_payed: date = Field(default=date.today())
    ammount: Decimal = Field(default=0, decimal_places=2)
    period: tuple[date, date]
    pay_code: str = Field(default="189")
    pay_model: str
    call_no: str


class Bill(BillBase, table=True):
    """Bill create model."""

    id: int | None = Field(default=None, primary_key=True)
    business_id: int = Field(default=None, foreign_key="business.id")
    business: Business = Relationship(back_populates="bills")
