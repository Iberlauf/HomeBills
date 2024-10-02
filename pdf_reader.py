"""Reads the .pdf file for data not provided by QR Code"""

from datetime import date, datetime
from pathlib import Path
from decimal import Decimal
import pymupdf
from pymupdf import Document

from qr_reader import extract_dates

pdfpath: Path = Path()


def clean_account_string(account_string: str) -> str:
    """Cleans the account string.

    Args:
        account_string (str): Input string representation of inegers that consist of three parts separated by spaces.

    Returns:
        str: 18-digit string representation of integer.
    """

    clean_string: str = account_string.strip().replace("\xad", " ")
    parts: list[str] = clean_string.split()
    result: str = f"{parts[0].strip()}{int(parts[1].strip()):013}{parts[2].strip()}"

    return result


def ammount_to_decimal(ammound_string: str) -> Decimal:
    """Returns ammount as decimal.

    Args:
        ammound_string (str): Block with the ammount.

    Returns:
        Decimal: Ammount as decimal.
    """
    return Decimal(value=ammound_string.strip().split()[-3])


def clean_call_string(call_string: str) -> str:
    """Cleans the call string.

    Args:
        call_string (str): Block with the call.

    Returns:
        str: _description_
    """
    return call_string.strip().split()[-1].replace("\xad", "")


def clean_period(period_string: str) -> tuple[date, date]:
    """Returns start and end date of the billing period.

    Args:
        period_string (str): Block with the period.

    Returns:
        tuple[date, date]: Start and end date of the billing period.
    """
    return (
        datetime.strptime(period_string.strip().split()[-3], "%d.%m.%Y").date(),
        datetime.strptime(period_string.strip().split()[-1], "%d.%m.%Y").date(),
    )


def sbb_pdf_reader(pdf_path: Path) -> tuple[date, date]:
    """Returns the billing period missing from the QR Code in the cable bill."""
    doc: Document = pymupdf.open(pdf_path)
    for doc_page in doc:
        txt_blocks: list[tuple] = doc_page.get_text(option="blocks")  # type: ignore
        period: tuple[date, date] = extract_dates(
            date_string=txt_blocks[7][4].strip().replace("\n", "")
        )
    return period


def eps_pdf_reader(pdf_path: Path) -> tuple[date, date]:
    """Returns the billing period missing from the QR Code in the electrical bill."""
    doc: Document = pymupdf.open(pdf_path)
    for doc_page in doc:
        txt_blocks: list[tuple] = doc_page.get_text(option="blocks")  # type: ignore
        period: tuple[date, date] = extract_dates(
            date_string=txt_blocks[9][4].strip().replace("\n", "")
        )
        break
    return period


def vodovod_pdf_reader(
    pdf_path: Path,
) -> list[str | Decimal | tuple[date, date]]:
    """Returns the billing period missing from the QR Code in the water bill."""
    doc: Document = pymupdf.open(pdf_path)
    for page in doc:
        txt_blocks: list[tuple] = page.get_text(option="blocks")  # type: ignore
        account: str = clean_account_string(account_string=txt_blocks[24][4])
        ammount: Decimal = ammount_to_decimal(ammound_string=txt_blocks[19][4])
        call_no: str = clean_call_string(call_string=txt_blocks[25][4])
        period: tuple[date, date] = clean_period(period_string=txt_blocks[7][4])

    return [account, ammount, call_no, period]
