import re
import logging
from pathlib import Path

import pdftotext
from PyPDF2 import PdfReader

num_dashes = 10
logging.basicConfig(level=logging.DEBUG)

### PDF Converting ###


def get_pdf_text2(filepath):
    pdf_reader = PdfReader(filepath)
    try:
        pages = [page.extract_text() for page in pdf_reader.pages]
    except Exception as e:
        print(f"Error of type {type(e)}: {e}")
        return ""
    text = "\n".join(pages)
    print("#", end="", flush=True)
    return text


def get_pdf_text(filepath):
    try:
        with open(filepath, "rb") as f:
            pdf = pdftotext.PDF(f)
            text = "\n".join([str(page) for page in pdf if page])
    except pdftotext.Error as e:
        logging.error(f"Exception of type {type(e)} while parsing {filepath}")
        return ""
    print("#", end="", flush=True)
    return text


def clean_filename(s: str) -> str:
    if not s.startswith("AOT"):
        s = "BTVS_" + s
    s = s.replace("Episode_", "")
    s = re.sub("%[0-9A-F]{2}", "", s)
    return s


def convert_all_pdfs() -> None:
    data_dir = Path("./data")
    pdf_dir = data_dir / "pdfs"
    text_dir = data_dir / "converted2"
    for filepath in pdf_dir.iterdir():
        transcript = get_pdf_text(filepath)
        stem = clean_filename(filepath.stem)
        target = text_dir / f"{stem}.txt"
        with open(target, "w") as f:
            f.write(transcript)


if __name__ == "__main__":
    convert_all_pdfs()
