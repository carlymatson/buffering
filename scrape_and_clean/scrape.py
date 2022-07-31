import re
import logging
from pathlib import Path
import time
from typing import Optional

import requests

from scraping_utils import json_cache, make_soup

logging.basicConfig(level=logging.INFO)


@json_cache("transcript_links.json")
def scrape_transcript_links() -> None:
    url = "https://www.bufferingthevampireslayer.com/transcriptions"
    soup = make_soup(url)
    all_links = soup.find_all("a")
    dropbox_links = [link["href"] for link in all_links if "dropbox" in link["href"]]
    return dropbox_links


def get_filename_from_link(url: str) -> str:
    url_suffix = url.split("/")[-1]
    url_stem = url_suffix.split(".pdf")[0]
    file_stem = re.sub("%20|\.", "_", url_stem)
    return file_stem + ".pdf"


def download_from_dropbox(link: str, filename: Optional[str] = None) -> None:
    pdf_dir = Path("./data/pdfs2")
    if filename is None:
        filename = get_filename_from_link(link)
    filepath = pdf_dir / filename

    logging.info(f"Create {filename}")
    # Change dl=0 to dl=1 to make link downloadable
    edited_link = link[:-1] + "1"
    r = requests.get(edited_link)
    with open(filepath, "wb") as f:
        for chunk in r.iter_content(chunk_size=1024):
            f.write(chunk)


def download_all_from_dropbox() -> None:
    dropbox_links = scrape_transcript_links()
    time.sleep(1)
    for url in dropbox_links:
        download_from_dropbox(url)
        time.sleep(1)


if __name__ == "__main__":
    download_all_from_dropbox()
