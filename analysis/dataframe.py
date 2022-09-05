import re
import csv
import json
from pathlib import Path
from datetime import datetime
import random

import pandas as pd
import streamlit as st


transcript_dir = Path("./data/cleaned5")


def load_episode_info_json():
    json_file = Path("data") / "episode_info.json"
    with open(json_file, "r") as f:
        data = json.load(f)
    return data


def load_air_dates():
    file = Path("data") / "all_episode_info.csv"
    rows = {}
    with file.open("r") as f:
        csvreader = csv.reader(f)
        for row in csvreader:
            show, ep_header, airdate, runtime = row
            ep_id, title = [s.strip() for s in ep_header.split(":", 1)]
            rows[(show, ep_id)] = (title, airdate, runtime)
    return rows


def clean_transcript(text):
    text = re.sub("\u200b", "", text)
    text = re.sub("", "\n", text)
    return text


def get_transcript_data(filepath):
    with filepath.open("r") as f:
        transcript = f.read().strip()
    transcript = clean_transcript(transcript)
    show, episode, body = transcript.split("\n", 2)
    episode = episode.replace("Episode ", "")
    # Find all dialogue based on pattern
    dialogue_pattern = "^(.*?): (.*)$"
    dialogue = re.findall(dialogue_pattern, body, flags=re.MULTILINE)
    return show, episode, dialogue

def get_episode_metadata(show, ep_header):
    ep_id = ep_header.split(":", 1)[0]
    ep_data = load_episode_info_json()
    matches = [ep for ep in ep_data if ep["show"].startswith(show[0]) and ep["ep_id"] == ep_id]
    if not matches:
        print("No matches:")
        print(ep_header)
    return matches[0] if matches else {}

def get_text_dataframe(filepath):
    show_header, ep_header, dialogue = get_transcript_data(filepath)
    meta = get_episode_metadata(show_header, ep_header)
    df = pd.DataFrame.from_records(dialogue, columns=["speaker", "line"])
    df["show"] = show_header
    df["ep_id"] = meta.get("ep_id", "?.?")
    df["title"] = meta.get("title", "Unknown Title")
    airdate = meta.get("airdate", "Jan 1, 2020") # FIXME What formatting is expected?
    dt = str(datetime.strptime(airdate, "%b %d, %Y").date())
    df["episode_date"] = pd.Timestamp(dt)
    df["air_date"] = airdate
    df["run_time"] = meta.get("runtime", "0 minutes")
    df["line_num"] = df.index + 1
    return df


def create_full_dataframe():
    df_list = [get_text_dataframe(filepath) for filepath in transcript_dir.iterdir()]
    full_df = pd.concat(df_list)
    full_df.sort_values(by=["episode_date", "line_num"], inplace=True)
    return full_df


def clean_jingle(text):
    jingle = text.upper()
    jingle = re.sub("[^A-Z]S$", "", jingle)  # Remove apostrophe S?
    jingle = re.sub('"', "", jingle) 
    jingle = re.sub('"', "", jingle)
    jingle = re.sub(".*FASHION WATCH.*", "FASHION WATCH", jingle)
    if "PATRIARCHY" in jingle:
        jingle = "THE PATRIARCHY"
    return jingle


def get_jingle_name(text):
    pattern = "\[([^\[\]]*?) jingle plays.*?\]"
    jingles = re.findall(pattern, text, flags=re.IGNORECASE)
    if len(jingles) == 0:
        return ""
    jingle = jingles[0]
    return clean_jingle(jingle)

# Where is this used?
def find_jingles(df):
    jingles = df[df["line"].str.contains("\[.*jingle plays.*\]")]
    jingles["jingle"] = df["line"].apply(get_jingle_name)
    cols = ["speaker", "line", "jingle", "ep_id", "air_date"]
    first_plays = jingles.groupby("jingle").first()
    cols = ["speaker", "line", "ep_id", "air_date", "episode_date"]
    st.write(first_plays[cols])
    data = {id: first_plays.loc[id, "air_date"] for id in first_plays.index}
    st.write(data)


def main():
    df = create_full_dataframe()
    df["line_num"] = df.index
    df.index = range(len(df))
    ###
    random_index = 10
    num_context = st.slider("Context", min_value=0, max_value=10, value=1, step=1)
    new_index = st.button("New Line")
    if new_index:
        random_index = random.choice(df.index)
    random_line = df.loc[
        random_index - num_context : random_index + num_context, ["speaker", "line"]
    ]
    st.table(random_line)
    episode = df.loc[random_index, ["ep_id", "title"]]
    st.write(episode)
