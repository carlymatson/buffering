import json
import logging
from typing import Optional

import requests
import bs4


def make_soup(url: str, text: Optional[str] = None) -> bs4.BeautifulSoup:
    if text is None:
        text = requests.get(url).text
    soup = bs4.BeautifulSoup(text, "html.parser")
    return soup


def load_from_json(file_name):
    try:
        with open(file_name, "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        return None
    return data


def json_cache(file_name):
    def decorator(func):
        def wrapper(*args, **kwargs):
            result = load_from_json(file_name)
            if result is not None:
                logging.info(f"Loading from cache {file_name}")
                return result
            logging.info(f"No cache called {file_name} found. Running function...")
            result = func(*args, **kwargs)
            # Write to cache
            with open(file_name, "w") as f:
                json.dump(result, f)
            return result

        return wrapper

    return decorator
