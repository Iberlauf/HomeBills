"""Mainn module."""

from datetime import date
from decimal import Decimal
from sqlmodel import Session, select
from pydantic import EmailStr
from database import create_db_and_tables, engine
from models import Address, User, Business, Bill, BusinessType


def create_address(strt: str, nmb: str, cty: str, pst: int):
    """Function that creates a new address."""

    with Session(bind=engine) as session:
        new_address = Address(
            street=strt,
            number=nmb,
            city=cty,
            postal_code=pst,
        )
        session.add(instance=new_address)
        session.commit()
        session.refresh(instance=new_address)


def create_user(
    f_name: str,
    l_name: str,
    e_mail: EmailStr,
    addressid: int,
):
    """Function that creates a new user."""

    with Session(bind=engine) as session:
        new_user = User(
            first_name=f_name,
            last_name=l_name,
            email=e_mail,
            address_id=addressid,
        )
        session.add(instance=new_user)
        session.commit()
        session.refresh(instance=new_user)


def create_business(
    business_name: str,
    bankaccount: int,
    pdfproducer: str,
    business_type: BusinessType,
    addressid: int,
):
    """Function that creates a new business."""

    with Session(bind=engine) as session:
        new_business = Business(
            name=business_name,
            bank_account=bankaccount,
            pdf_producer=pdfproducer,
            type=business_type,
            address_id=addressid,
        )
        session.add(instance=new_business)
        session.commit()
        session.refresh(instance=new_business)


def create_bill(
    bill_name: str,
    bill_payed: bool,
    datepayed: date,
    bill_ammount: Decimal,
    businessid: int,
):
    """Function that creates a new bill."""

    with Session(bind=engine) as session:
        new_bill = Bill(
            name=bill_name,
            payed=bill_payed,
            date_payed=datepayed,
            ammount=bill_ammount,
            business_id=businessid,
        )
        session.add(instance=new_bill)
        session.commit()
        session.refresh(instance=new_bill)


def get_address(address_id: int) -> Address | None:
    """Function that selects an address."""
    with Session(bind=engine) as session:
        address = session.get(entity=Address, ident=address_id)
        if address:
            return address
        return None


def get_user(user_id: int) -> User | None:
    """Function that selects a user."""
    with Session(bind=engine) as session:
        user = session.get(entity=User, ident=user_id)
        if user:
            return user
        return None


def get_buiness(business_id: int) -> Business | None:
    """Function that selects a business."""
    with Session(bind=engine) as session:
        business = session.get(entity=Business, ident=business_id)
        if business:
            return business
        return None


def select_business_by_account(account: int) -> Business | None:
    """Function that selects a business."""
    with Session(bind=engine) as session:
        business = session.exec(
            select(Business).where(Business.bank_account == account)
        ).first()
        if business:
            return business
        return None


def main() -> None:
    """Main function."""

    create_db_and_tables()
    # get_user(user_id=1)
    # get_address(address_id=1)


if __name__ == "__main__":
    main()
