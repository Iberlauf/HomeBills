"""Module for creating SQLModel instances."""

from datetime import date
from decimal import Decimal
from pydantic import EmailStr, HttpUrl
from sqlmodel import Session
from database import engine
from models import Address, Bill, Business, BusinessType, User


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


def create_business(  # pylint: disable=(R0913:too-many-arguments)
    business_name: str,
    bankaccount: int,
    pdfproducer: str,
    business_type: BusinessType,
    addressid: int,
    business_url: HttpUrl,
):
    """Function that creates a new business."""

    with Session(bind=engine) as session:
        new_business = Business(
            name=business_name,
            bank_account=bankaccount,
            pdf_producer=pdfproducer,
            type=business_type,
            address_id=addressid,
            url=business_url,
        )
        session.add(instance=new_business)
        session.commit()
        session.refresh(instance=new_business)


def create_bill(  # pylint: disable=(R0913:too-many-arguments)
    bill_name: str,
    bill_payed: bool,
    datepayed: date,
    bill_ammount: Decimal,
    paycode: str,
    paymodel: str,
    callno: str,
    businessid: int,
    billing_period: tuple[date, date],
):
    """Function that creates a new bill."""

    with Session(bind=engine) as session:
        new_bill = Bill(
            name=bill_name,
            payed=bill_payed,
            date_payed=datepayed,
            ammount=bill_ammount,
            pay_code=paycode,
            pay_model=paymodel,
            call_no=callno,
            business_id=businessid,
            period=billing_period,
        )
        session.add(instance=new_bill)
        session.commit()
        session.refresh(instance=new_bill)
