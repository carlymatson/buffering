import re
import logging
from pathlib import Path

# import pdftotext
from PyPDF2 import PdfReader

from text_cleaning import clean_transcript

num_dashes = 10
logging.basicConfig(level=logging.DEBUG)

### PDF Converting ###

DATA_DIR = Path("./data")
PDF_DIR = DATA_DIR / "pdfs"
TEXT_DIR = DATA_DIR / "converted5"


def get_pdf_with_pypdf2(filepath):
    pdf_reader = PdfReader(filepath)
    try:
        pages = [page.extract_text() for page in pdf_reader.pages]
    except Exception as e:
        print(f"Error of type {type(e)}: {e}")
        return ""
    text = "\n".join(pages)
    print("#", end="", flush=True)
    return text


# def get_pdf_text(filepath):
# try:
# with open(filepath, "rb") as f:
# pdf = pdftotext.PDF(f)
## text = "\n".join([str(page) for page in pdf if page])
# pages = [str(page) for page in pdf if page]
# except pdftotext.Error as e:
# logging.error(f"Exception of type {type(e)} while parsing {filepath}")
# return ""
# text = "".join(pages)
# print("#", end="", flush=True)
# return text


def clean_filename(s: str) -> str:
    if not s.startswith("AOT"):
        s = "BTVS_" + s
    s = s.replace("Episode_", "")
    s = re.sub("%[0-9A-F]{2}", "", s)
    s = re.sub("__+", "_", s)
    return s


def convert_all_pdfs() -> None:
    for filepath in PDF_DIR.iterdir():
        # transcript = get_pdf_text(filepath)
        transcript = get_pdf_with_pypdf2(filepath)
        # transcript = clean_transcript(transcript)
        stem = clean_filename(filepath.stem)
        target = TEXT_DIR / f"{stem}.txt"
        with open(target, "w") as f:
            f.write(transcript)


if __name__ == "__main__":
    # convert_all_pdfs()
    # filename = "data/pdfs/BTVS_7_18_Dirty_Girls.pdf"
    filename = "data/pdfs/BTVS_7_17_Lies_My_Parents_Told_Me.pdf"
    text = get_pdf_with_pypdf2(filename)
    print(text)
