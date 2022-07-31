from collections import Counter
import re
from pathlib import Path
from typing import Iterable

import pandas as pd
import streamlit as st
import diff_viewer

import text_cleaning


def get_transcript():
    ep = "buffy_2_14_innocence.txt"
    eps = Path("./data/cleaned")
    filepath = eps / ep
    with filepath.open("r") as f:
        text = f.read()
    return text


def play_with_diffs():
    text = get_transcript()
    col1, col2 = st.columns(2)
    with col1:
        pattern = st.text_input("Pattern", value="")
    with col2:
        sub = st.text_input("Substitution", value="")
    old_text = text
    new_text = re.sub(pattern, sub, old_text, flags=re.MULTILINE)
    diff_viewer.diff_viewer(old_text=old_text, new_text=new_text, lang="none")


def get_transcript(ep: Path) -> str:
    with ep.open("r") as f:
        text = f.read()
    return text


def select_transcript():
    text_dir = Path("./data/converted2")
    options = [f for f in text_dir.iterdir()]
    ep = st.selectbox("Episode", options=options, format_func=lambda f: f.stem)
    text = get_transcript(ep)
    return text


def get_all_transcripts():
    text = ""
    text_dir = Path("./data/converted2")
    options = [f for f in text_dir.iterdir()]
    for file in options:
        text += get_transcript(file)
    return text


def process(text: str) -> str:
    text = text_cleaning.clean_characters(text)
    text = text_cleaning.clean_speakers(text)
    text = text_cleaning.clean_lines(text)
    return text


def examine_processing(text, func):
    new_text = func(text)
    diff_viewer.diff_viewer(text, new_text, lang="none")
    return new_text


def investigate():
    text = get_all_transcripts()
    text = process(text)
    sanity_checks(text)
    return text


def get_count_df(items: Iterable, label: str = "Item") -> None:
    counts = Counter(items)
    df = pd.DataFrame.from_records(list(counts.items()), columns=[label, "Count"])
    return df


def or_group(re_list: Iterable[str]) -> str:
    or_re = "|".join(re_list)
    group_re = "(?:" + or_re + ")"
    return group_re


def get_dialog_re():
    name_re = "[A-Z][a-z]+"
    full_name_re = f"{name_re}(?: {name_re})*"
    speaker_res = [
        f"{full_name_re}",
        f"{full_name_re} and {full_name_re}",
        f"{full_name_re}/{full_name_re}",
    ]
    dialog_re = or_group(speaker_res) + "(?=: )"
    return dialog_re


def get_all_speakers(text):
    dialog_re = get_dialog_re()
    matches = re.findall("^" + dialog_re, text, re.MULTILINE)
    return matches


def get_notes_re(full_line: bool = False):
    non_brackets = "[\\[\\]]"
    notes_re = f"\\[{non_brackets}+\\]"
    if full_line:
        notes_re = "^" + notes_re + "$"
    return notes_re


def find_bad_lines(text):  # FIXME Not working
    pattern = "^[^:]*$"
    bad_lines = re.findall(pattern, text, flags=re.MULTILINE)
    return bad_lines


def sanity_checks(text: str) -> None:
    col1, col2, col3 = st.columns(3)
    with col1:
        df = get_count_df(list(text))
        df["Unicode"] = df["Item"].apply(lambda x: ord(x))
        st.write(df)
    with col2:
        st.write(get_count_df(get_all_speakers(text)))
    with col3:
        st.write(get_count_df(find_bad_lines(text)))


if __name__ == "__main__":
    investigate()

# play_with_diffs()
