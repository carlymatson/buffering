import csv
import re
from pprint import pprint
import logging

from scraping_utils import make_soup

logging.basicConfig(level=logging.INFO)


def extract_episode_div(soup):
    date_class = "v-list-item__subtitle text-grey4 episodeInfo"
    ep_header_class = "text-truncate text-grey5"
    date_header_div = soup.find_all("div", {"class": date_class})[0]
    ep_header_div = soup.find_all("div", {"class": ep_header_class})[0]
    runtime, date = [s.strip() for s in date_header_div.text.split("|")]
    ep_header = ep_header_div.text.strip()
    return ep_header, date, runtime


def adhoc(soup):
    text = str(soup)
    eps = re.findall("1.01: Welcome to the Hellmouth", text)
    print(eps)


def scrape_series_info(html_doc):
    with open(html_doc, "r") as f:
        text = f.read()
    soup = make_soup("", text=text)
    group_class = "v-list-item__content pa-0 mr-4 mr-md-6"
    # adhoc(soup)
    # return
    possible_groups = soup.find_all("div", {"class": group_class})
    ep_info = [extract_episode_div(div) for div in possible_groups]
    return ep_info


aot_filename = "data/angel_on_top_ep_info.txt"
buffering_filename = "data/buffering_ep_info.txt"

buff_info = [
    ["Buffering the Vampire Slayer"] + list(ep_info)
    for ep_info in scrape_series_info(buffering_filename)
]
aot_info = [
    ["Angel On Top"] + list(ep_info)
    for ep_info in scrape_series_info(buffering_filename)
]

with open("data/all_episode_info.csv", "w") as f:
    csvwriter = csv.writer(f)
    csvwriter.writerows(buff_info)
    csvwriter.writerows(aot_info)
