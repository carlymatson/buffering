import re
import json
from datetime import datetime
from typing import Optional

import streamlit as st
from analysis.my_timeline import timeline

from analysis.dataframe import load_air_dates

season_dates = [
    ("Sep 1, 2016", "Jan 4, 2017"),
    ("Jan 11, 2017", "Jul 19, 2017"),
    ("Sep 6, 2017", "Apr 4, 2018"),
    ("May 23, 2018", "Jul 23, 2019"),
    ("Sep 18, 2019", "Sep 30, 2020"),
    ("Oct 7, 2020", "Oct 13, 2021"),
    ("Nov 3, 2021", "Jul 9, 2022"),
]


def load_interview_links():
    with open("data/interview_info.json", "r") as f:
        data = json.load(f)
    return data


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
    height = 600
    timeline(data, height=height)


def is_interview(ep_title: str) -> str:
    is_interview = "Interview" in ep_title or "Amber" in ep_title
    return is_interview


def load_jingle_data():
    filename = "data/jingle_info.json"
    with open(filename, "r") as f:
        data = json.load(f)
    return data


def format_lyrics(lyrics):
    if not lyrics:
        return ""
    lyrics_html = "<i>" + "<br />".join(lyrics) + "</i>"
    return lyrics_html


def get_jingle_events(data):
    events = [
        Event(
            headline=name,
            start_date=jingle["debut_date"],
            group="Jingle Debut",
            media=jingle.get("image_url", None),
            text=format_lyrics(jingle.get("lyrics", "")),
        )
        for name, jingle in data.items()
    ]
    return events


def get_interviewee(ep_title) -> str:
    if "Interview" in ep_title or "Amber" in ep_title:
        print(f"Interview: {ep_title}")
        _, name = ep_title.split(" with ")
        # name = ep_title
    else:
        return ep_title
    return name


def get_interview_events(ep, airdate):
    links = load_interview_links()
    matching_links = [link for person, link in links.items() if person in ep]
    url = matching_links[0] if matching_links else None
    interview_events = Event(
        headline=ep,
        start_date=airdate,
        group="Interview",
        media=url,
    )
    return interview_events


def show_special_episodes():
    # Load data, parse, parse
    air_dates = load_air_dates()
    interviews = [
        (get_interviewee(info[0]), info[1])
        for (show, ep_id), info in air_dates.items()
        if ep_id.startswith("0") and is_interview(info[0])
    ]
    special_eps = [
        (info[0], info[1])
        for (show, ep_id), info in air_dates.items()
        if ep_id.startswith("0") and not is_interview(info[0])
    ]
    interview_events = [
        get_interview_events(ep, airdate) for (ep, airdate) in interviews
    ]
    special_ep_events = [
        Event(
            headline=ep,
            start_date=airdate,
            group="Special Episode",
        )
        for (ep, airdate) in special_eps
    ]
    jingle_data = load_jingle_data()
    jingle_events = get_jingle_events(jingle_data)
    events = interview_events + special_ep_events + jingle_events
    groups = set([ev.group for ev in events])
    starting_groups = ["Interview", "Jingle Debut"]
    with st.sidebar:
        display_groups = st.multiselect(
            "Display", options=groups, default=starting_groups
        )
    display_events = [ev for ev in events if ev.group in display_groups]
    display_dates(display_events)


def main():
    show_special_episodes()
