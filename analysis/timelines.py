import json
from datetime import datetime
import random
from pprint import pprint
from typing import Optional

import streamlit as st
from streamlit_timeline import timeline

from analysis.dataframe import create_full_dataframe, load_air_dates


season_dates = [
    ("Sep 1, 2016", "Jan 4, 2017"),
    ("Jan 11, 2017", "Jul 19, 2017"),
    ("Sep 6, 2017", "Apr 4, 2018"),
    ("May 23, 2018", "Jul 23, 2019"),
    ("Sep 18, 2019", "Sep 30, 2020"),
    ("Oct 7, 2020", "Oct 13, 2021"),
    ("Nov 3, 2021", "Jul 9, 2022"),
]


JINGLE_IMAGES = dict(
    anya="https://images.squarespace-cdn.com/content/v1/596014bd36e5d37e136fa33f/1573678066331-Q5V0MV27L5SSTE9G609O/hqdefault.jpg?format=500w",
    ben_is_glory="https://images.squarespace-cdn.com/content/v1/596014bd36e5d37e136fa33f/1588386397958-S2VXXV3B5WYACJVHK213/Ben+Is+Glory.jpg?format=750w",
    cordelia="https://images.squarespace-cdn.com/content/v1/596014bd36e5d37e136fa33f/1507653079880-9RCB1QN8LZSSO6RTEKFY/cordelia.jpg?format=1000w",
    detective_angel="https://images.squarespace-cdn.com/content/v1/596014bd36e5d37e136fa33f/1522948370982-QORHYWEANSS1MV4JT7N7/detective+angel.jpg?format=750w",
    drusilla="https://images.squarespace-cdn.com/content/v1/596014bd36e5d37e136fa33f/1507653090156-Z2CEHNXWEU7JNX1JK57F/drusilla.jpg?format=750w",
    faith="https://images.squarespace-cdn.com/content/v1/596014bd36e5d37e136fa33f/1522948107003-WO4KTUWXSU160JXR1ZJP/Faith-Lehane-Buffy-Vampire-Slayer-c.jpg?format=500w",
    giles="https://images.squarespace-cdn.com/content/v1/596014bd36e5d37e136fa33f/1569973934022-U0RSXS2OTDKJQN7VW1BJ/giles-forearms-gah-1024x774.png?format=500w",
    go_away_riley="https://images.squarespace-cdn.com/content/v1/596014bd36e5d37e136fa33f/1569973940180-QHJ4EWC3MTOGV1C1QXTG/RileyFinn.JPG.jpg?format=750w",
    hellmath="https://images.squarespace-cdn.com/content/v1/596014bd36e5d37e136fa33f/1569974446038-W8YJ2M75EBF4WLO7LNC2/hellmath.jpg?format=750w",
    kristin_noeline="https://images.squarespace-cdn.com/content/v1/596014bd36e5d37e136fa33f/1569973982905-7P6ASCNQ54KR5QPA4ONK/buffy-prom-2019-262.jpg?format=750w",
    patrol_cat="https://images.squarespace-cdn.com/content/v1/596014bd36e5d37e136fa33f/1507656631429-5TG4ONVKCX3PXT57TT0N/IMG_0494.JPG?format=750w",
    sexual_tension_award="https://images.squarespace-cdn.com/content/v1/596014bd36e5d37e136fa33f/1507653359055-50AVZYJ0YMTKE0GE5VVK/sexual+tension.jpg?format=750w",
    spike="https://images.squarespace-cdn.com/content/v1/596014bd36e5d37e136fa33f/1507653099207-H63WHH354QT8W9M2HTG7/spike.png?format=750w",
    spike_and_dru="https://images.squarespace-cdn.com/content/v1/596014bd36e5d37e136fa33f/1507653117066-6B4E2PP80YUCRZRWW2GI/spikedru.jpg?format=1000w",
    spooky_news="https://images.squarespace-cdn.com/content/v1/596014bd36e5d37e136fa33f/1569973893569-R2TOLY6PG93IJN42DPP6/buffy-the-vampire-slayer-boo.png?format=750w",
    the_green_mug_song="https://images.squarespace-cdn.com/content/v1/596014bd36e5d37e136fa33f/1507653125041-J1CA5RJWHPQ5INXSYFWR/green+mug.jpg?format=750w",
    the_patriarchy="https://images.squarespace-cdn.com/content/v1/596014bd36e5d37e136fa33f/1507653213603-S8HMSFHOPZI48L0GMXB5/patriarchy.png?format=1000w",
    vampire_willow="https://images.squarespace-cdn.com/content/v1/596014bd36e5d37e136fa33f/1522948469651-V5ZTJIXH5UB5OIPEKDR9/vamp+willow.jpg?format=750w",
    willow="https://images.squarespace-cdn.com/content/v1/596014bd36e5d37e136fa33f/1507653107683-QAI2SH3PQ4XIP7F08ZOE/willow.jpg?format=500w",
    willow_and_tara="https://images.squarespace-cdn.com/content/v1/596014bd36e5d37e136fa33f/1569973948524-VB64CBNWJZFPE5ZZPM61/tara-willow-candle.jpg?format=750w",
)


class Event:
    def __init__(
        self,
        start_date,
        headline: Optional[str] = None,
        text: Optional[str] = None,
        group: str = "Buffering the Vampire Slayer",
        media: Optional[str] = None,
    ):
        self.start_date = parse_date(start_date)
        text_obj = {"headline": headline, "text": text}
        self.text = text_obj
        self.group = group
        self.media = media

    def to_dict(self):
        non_null_attrs = {
            key: getattr(self, key)
            for key in ["start_date", "text", "group"]
            if getattr(self, key) is not None
        }
        if self.media is not None:
            non_null_attrs["media"] = dict(url=self.media)
        return non_null_attrs


def parse_date(date_string):
    date = datetime.strptime(date_string, "%b %d, %Y")
    date_parts = {part: getattr(date, part) for part in ["year", "month", "day"]}
    return date_parts


def display_dates(events):
    global season_dates
    eras = [
        dict(
            start_date=parse_date(dates[0]),
            end_date=parse_date(dates[1]),
            text=dict(headline=f"Season {idx+1}"),
        )
        for idx, dates in enumerate(season_dates)
    ]
    event_dicts = [ev.to_dict() for ev in events]
    data = {"events": event_dicts, "eras": eras}
    # height = st.slider("Height", min_value=400, max_value=700, value=500)
    height = 600
    timeline(data, height=height)


def ep_type(ep: str) -> str:
    if "Interview" in ep:
        return "Interview"
    if "Mailbag" in ep:
        return "Mailbag"
    return "Special Episode"


def load_jingle_data():
    with open("data/jingle_data.json", "r") as f:
        data = json.load(f)
    return data


def get_jingle_image(name):
    words = [w.lower() for w in name.split(" ")]
    key = "_".join(words)
    return JINGLE_IMAGES.get(key, None)


def show_special_episodes():
    air_dates = load_air_dates()
    special_eps = [
        (f"{ep_id}: {info[0]}", info[1])
        for (show, ep_id), info in air_dates.items()
        if ep_id.startswith("0")
    ]
    ep_types = {ep: ep_type(ep) for (ep, _) in special_eps}
    events = [
        Event(headline=ep, start_date=airdate, group=ep_types[ep])
        for (ep, airdate) in special_eps
    ]
    jingle_debut_data = load_jingle_data()
    jingle_debuts = [
        Event(
            headline=name,
            start_date=airdate,
            group="Jingle Debuts",
            media=get_jingle_image(name),
        )
        for (name, airdate) in jingle_debut_data.items()
    ]
    events = events + jingle_debuts
    groups = set([ev.group for ev in events])
    with st.sidebar:
        display_groups = st.multiselect("Display", options=groups, default=groups)
    display_events = [ev for ev in events if ev.group in display_groups]
    display_dates(display_events)


def main():
    show_special_episodes()
