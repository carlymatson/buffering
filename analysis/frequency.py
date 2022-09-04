import re

import streamlit as st
import seaborn as sns

from analysis.dataframe import create_full_dataframe


def count_pattern(text, pattern):
    matches = re.findall(pattern, text, flags=re.IGNORECASE)
    return len(matches)


def main():
    df = create_full_dataframe()
    pattern = st.text_input("Pattern")
    regex_df = df[df["line"].str.contains(pattern, flags=re.IGNORECASE)]
    date_counts = (
        regex_df.groupby("episode_date")
        .count()
        .rename(columns={"line": "count"})["count"]
    )
    st.bar_chart(date_counts)
    st.write(regex_df)
