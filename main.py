"""Mainn module."""

from datetime import date
from decimal import Decimal
from sqlmodel import Session, select
from pydantic import EmailStr
from database import create_db_and_tables, engine
from models import Address, User, Business, Bill, BusinessType


def create_address(strt: str, nmb: str, cty: str, pst: int):
    """Function that creates a new address."""

    with Session(engine) as session:
        new_address = Address(
            street=strt,
            number=nmb,
            city=cty,
            postal_code=pst,
        )
        session.add(new_address)
        session.commit()
        session.refresh(new_address)


def create_user(
    f_name: str,
    l_name: str,
    e_mail: EmailStr,
    addressid: int,
):
    """Function that creates a new user."""

    with Session(engine) as session:
        new_user = User(
            first_name=f_name,
            last_name=l_name,
            email=e_mail,
            address_id=addressid,
        )
        session.add(new_user)
        session.commit()
        session.refresh(new_user)


def create_business(  # pylint: disable=(R0913:too-many-arguments)
    business_name: str,
    contactemail: EmailStr,
    bankaccount: int,
    pdfproducer: str,
    business_type: BusinessType,
    addressid: int,
):
    """Function that creates a new business."""

    with Session(engine) as session:
        new_business = Business(
            name=business_name,
            contact_email=contactemail,
            bank_account=bankaccount,
            pdf_producer=pdfproducer,
            type=business_type,
            address_id=addressid,
        )
        session.add(new_business)
        session.commit()
        session.refresh(new_business)


def create_billl(
    bill_name: str,
    bill_payed: bool,
    datepayed: date,
    bill_ammount: Decimal,
    businessid: int,
):
    """Function that creates a new bill."""

    with Session(engine) as session:
        new_bill = Bill(
            name=bill_name,
            payed=bill_payed,
            date_payed=datepayed,
            ammount=bill_ammount,
            business_id=businessid,
        )
        session.add(new_bill)
        session.commit()
        session.refresh(new_bill)


def main() -> None:
    """Main function."""

    create_db_and_tables()


if __name__ == "__main__":
    main()
