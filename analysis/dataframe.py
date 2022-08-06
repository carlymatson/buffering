import re
import csv
from pathlib import Path
from datetime import datetime
import random

import pandas as pd
import streamlit as st


transcript_dir = Path("./data/cleaned")


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


def get_text_dataframe(filepath):
    air_dates = load_air_dates()
    with filepath.open("r") as f:
        show = f.readline().strip()
        ep_header = f.readline().strip()
        text = f.read()
    ep_header = ep_header.replace("Episode ", "")
    ep_id, _ = [part.strip() for part in ep_header.split(":", 1)]
    ep_info = air_dates.get((show, ep_id), None)
    if ep_info is None:
        print(f"Couldn't find {(show, ep_id)}")
        return
    dialogue_pattern = "^(.*?): (.*)$"
    dialogue = re.findall(dialogue_pattern, text, flags=re.MULTILINE)
    df = pd.DataFrame.from_records(dialogue, columns=["speaker", "line"])
    df["show"] = show
    df["ep_id"] = ep_id
    df["title"] = ep_info[0]
    dt = str(datetime.strptime(ep_info[1], "%b %d, %Y").date())
    df["air_date2"] = pd.Timestamp(dt)
    df["air_date"] = ep_info[1]
    df["run_time"] = ep_info[2]
    return df


def create_full_dataframe():
    df_list = []
    for filepath in transcript_dir.iterdir():
        df = get_text_dataframe(filepath)
        df_list.append(df)
    full_df = pd.concat(df_list)
    full_df.sort_values(by="air_date2", inplace=True)
    return full_df


def clean_jingle(text):
    jingle = text.upper()
    jingle = re.sub("[^A-Z]S$", "", jingle)
    jingle = re.sub('"', "", jingle)
    jingle = re.sub("HELL MATH", "HELLMATH", jingle)
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


def find_jingles(df):
    jingles = df[df["line"].str.contains("\[.*jingle plays.*\]")]
    jingles["jingle"] = df["line"].apply(get_jingle_name)
    cols = ["speaker", "line", "jingle", "ep_id", "air_date"]
    first_plays = jingles.groupby("jingle").first()
    cols = ["speaker", "line", "ep_id", "air_date", "air_date2"]
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
