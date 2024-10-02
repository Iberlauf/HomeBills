"""Module for creating SQLModel instances."""

from datetime import date, datetime
from decimal import Decimal
from pathlib import Path

from pydantic import EmailStr, HttpUrl
from sqlmodel import Session

from database import engine
from main import select_business_by_account
from models import Address, Bill, Business, BusinessType, User
from pdf_reader import eps_pdf_reader, sbb_pdf_reader, vodovod_pdf_reader
from qr_reader import clean_decimal, extract_dates, qr_reader


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


def new_bill_from_pdf(pdf_path: Path) -> None:
    """Creates a new Bill class instance/database entry from .pdf file."""
    results: list[dict[str, str]] | None = qr_reader(pdf_path=pdf_path)
    if results is not None:
        result_dict: dict = results[0]
        new_ammount: Decimal = clean_decimal(ammount_str=result_dict["I"])
        new_business: Business | None = select_business_by_account(
            account=int(result_dict["R"])
        )
        new_pay_code: str = results[0]["SF"]
        if result_dict["S"]:
            new_period: tuple[date, date] = extract_dates(date_string=result_dict["S"])
        elif new_business and new_business.name == "SBB":
            new_period = sbb_pdf_reader(pdf_path=pdf_path)
        elif new_business and new_business.name == "EPS":
            new_period = eps_pdf_reader(pdf_path=pdf_path)
        if results[0]["RO"].startswith("97"):
            new_model: str = results[0]["RO"][:2]
            new_call_no: str = results[0]["RO"][2:]
        else:
            new_model: str = ""
            new_call_no: str = results[0]["RO"]
    else:
        new_business: Business | None = select_business_by_account(
            account=int(vodovod_pdf_reader(pdf_path=pdf_path)[0])  # type: ignore
        )
        new_ammount: Decimal = vodovod_pdf_reader(pdf_path=pdf_path)[1]  # type: ignore
        new_model: str = ""
        new_call_no: str = vodovod_pdf_reader(pdf_path=pdf_path)[2]  # type: ignore
        new_period: tuple[date, date] = vodovod_pdf_reader(pdf_path=pdf_path)[3]  # type: ignore

    if new_business and new_business.id is not None:
        with Session(bind=engine) as session:
            new_bill = Bill(
                name=f"{new_business.name} from {new_period[0]} to {new_period[1]}",
                payed=True,
                date_payed=datetime.today(),
                ammount=new_ammount,
                pay_code=new_pay_code,
                pay_model=new_model,
                call_no=new_call_no,
                business_id=new_business.id,
                period=new_period,
            )
            session.add(instance=new_bill)
            session.commit()
            session.refresh(instance=new_bill)
