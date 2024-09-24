"""Get all the QR codes from .pdf file and read."""

from pathlib import Path
import pandas as pd
from pdf2image import convert_from_bytes
from PIL.Image import Image
from PyPDF2 import PdfReader
from pyzbar import pyzbar


pdf_path: Path = Path()
pdfPages: PdfReader = PdfReader(stream=pdf_path)
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
        data_list: list[str] = raw_data.split("|")
        result_list: list[dict[str, str]] = [{}]
        for strng in data_list:
            if "|" in strng:
                key, val = strng.split(":", 1)
                if key in result_list[-1]:
                    result_list.append({})
                result_list[-1][key] = val

if result_list:
    print(result_list[0])
df: pd.DataFrame = pd.DataFrame.from_dict(data=result_list, orient="columns")
print(df.head())
