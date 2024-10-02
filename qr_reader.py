"""Get all the QR codes from .pdf file,
read them and create a bill instance
if the QR code is a valid NBS IPS code.
"""

import re
from datetime import date, datetime
from decimal import Decimal
from pathlib import Path

# import pandas as pd
from pdf2image import convert_from_bytes
from PIL.Image import Image
from pyzbar import pyzbar


def clean_decimal(ammount_str: str) -> Decimal:
    """Function for cleaning the ammount string.

    Args:
        ammount_str (str): String representation of the ammount.

    Returns:
        Decimal: Decimal representation of the ammount.
    """
    return Decimal(value=ammount_str.removeprefix("RSD").replace(",", ".").strip())


def extract_dates(date_string: str) -> tuple[date, date]:
    """Extracts dates from string.

    Args:
        date_string (str): String that has two dates.

    Returns:
        tuple[date, date]: Tuple of two dates.
    """
    date_pattern: str = r"(\d{2}\.\d{2}\.\d{4})"
    matches: list[str] = re.findall(pattern=date_pattern, string=date_string)
    dates: list[date] = [
        datetime.strptime(date_str, "%d.%m.%Y").date() for date_str in matches
    ]

    return dates[0], dates[1]


def qr_reader(pdf_path: Path) -> list[dict[str, str]] | None:
    """Get all the QR codes from .pdf file and return them as a list of dictionaries.

    Args:
        pdf_path (Path): Path object to .pdf file.

    Returns:
        list[dict[str, str]] | None:
        List of dictionaries from the .pdf file
        if there is a valid NBS IPS QR code in said file.
    """
    with open(file=pdf_path, mode="rb") as f:
        page_bytes: bytes = f.read()
    pages: list[Image] = convert_from_bytes(pdf_file=page_bytes, dpi=600)

    counter: int = 0
    output: list[bytes] = []
    for page in pages:
        val: list[pyzbar.Decoded] = pyzbar.decode(image=page)
        if val:
            # found a qr code
            data: bytes = val[0][0]
            if counter != 0:
                output.append(data)
        counter += 1

    output.append(data)

    for name in output:
        raw_data: str = name.decode(encoding="utf-8")
        if "|" in raw_data:
            data_list: list[str] = raw_data.split(sep="|")
            result_list: list[dict[str, str]] = [{}]
            for strng in data_list:
                if ":" in strng:
                    key, val = strng.split(sep=":", maxsplit=1)  # type: ignore
                    if key in result_list[-1]:
                        result_list.append({})
                    result_list[-1][key] = val  # type: ignore
    if result_list:
        return result_list
    return None

    # df: pd.DataFrame = pd.DataFrame.from_dict(data=results, orient="columns")  # type: ignore
    # print(df.head())
