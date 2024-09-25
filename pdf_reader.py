"""Get all the QR codes from .pdf file and read."""

from pathlib import Path
from decimal import Decimal
from datetime import date

# import pandas as pd
from pdf2image import convert_from_bytes
from PIL.Image import Image
from pyzbar import pyzbar


from main import select_business_by_account, create_bill


def ammount_cleaner(ammount_str: str) -> Decimal:
    """Clean the ammount from the string."""
    return Decimal(ammount_str.removeprefix("RSD").replace(",", "."))


def pdf_reader(pdf_path: Path) -> list[dict[str, str]] | None:
    """Get all the QR codes from .pdf file and read."""
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


pdfpath: Path = Path()

results = pdf_reader(pdf_path=pdfpath)
if results:
    result_dict: dict = results[0]
    dict_amount = ammount_cleaner(result_dict["I"])
    business = select_business_by_account(account=int(result_dict["R"]))
    if business and business.id is not None:
        create_bill(
            bill_name=f"{business.type.value} - {date.today().strftime('%B')}",
            bill_payed=True,
            datepayed=date.today(),
            bill_ammount=dict_amount,
            businessid=business.id,
        )

    # df: pd.DataFrame = pd.DataFrame.from_dict(data=results, orient="columns")  # type: ignore
    # print(df.head())
