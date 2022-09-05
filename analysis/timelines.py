import json
from datetime import datetime
from typing import Optional

import streamlit as st

from analysis.js_timeline import timeline


season_dates = [
    ("Sep 1, 2016", "Jan 4, 2017"),
    ("Jan 11, 2017", "Jul 19, 2017"),
    ("Sep 6, 2017", "Apr 4, 2018"),
    ("May 23, 2018", "Jul 23, 2019"),
    ("Sep 18, 2019", "Sep 30, 2020"),
    ("Oct 7, 2020", "Oct 13, 2021"),
    ("Nov 3, 2021", "Jul 9, 2022"),
]



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



def format_lyrics(lyrics):
    if not lyrics:
        return ""
    lyrics_html = "<i>" + "<br />".join(lyrics) + "</i>"
    return lyrics_html


def is_interview(ep_title: str) -> str:
    is_interview = "Interview" in ep_title or "Amber" in ep_title
    return is_interview


def get_interviewee(ep_title) -> str:
    if "Interview" in ep_title or "Amber" in ep_title:
        _, name = ep_title.split(" with ")
    else:
        return ep_title
    return name

def timeline_widget(events, default_groups = ["Interview", "Jingle Debut", "Special Episode"]):
    # Eras
    global season_dates
    eras = [
        dict(
            start_date=parse_date(dates[0]),
            end_date=parse_date(dates[1]),
            text=dict(headline=f"Season {idx+1}"),
        )
        for idx, dates in enumerate(season_dates)
    ]
    # Events
    groups = set([ev.group for ev in events])
    starting_groups = [g for g in default_groups if g in groups]
    with st.sidebar:
        display_groups = st.multiselect(
            "Display", options=groups, default=starting_groups
        )
    event_dicts = [ev.to_dict() for ev in events if ev.group in display_groups]
    data = {"events": event_dicts, "eras": eras}
    height = 600
    timeline(data, height=height)



def show_special_episodes():
    with open("data/episode_info.json", "r") as f:
        episode_info = json.load(f)
    with open("data/jingle_info.json", "r") as f:
        jingle_data = json.load(f)
    interview_events = [
        Event(
            headline = get_interviewee(info["title"]), 
            start_date=info["airdate"],
            group="Interview",
            media = info.get("spotify_url", None),
        ) for info in episode_info
        if is_interview(info["title"])
    ]
    special_ep_events = [
        Event(
            headline = info["title"],
            start_date=info["airdate"],
            group = "Special Episode"
        )
        for info in episode_info
        if info["ep_id"].startswith("0") and not is_interview(info["title"])
    ]
    jingle_events = [
        Event(
            headline=name,
            start_date=jingle["debut_date"],
            group="Jingle Debut",
            media=jingle.get("image_url", None),
            text=format_lyrics(jingle.get("lyrics", "")),
        )
        for name, jingle in jingle_data.items()
    ]
    events = interview_events + special_ep_events + jingle_events
    timeline_widget(events)


def main():
    show_special_episodes()
