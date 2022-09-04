import re
import math

import streamlit as st

from analysis import dataframe

st.set_page_config(layout="wide")


def about():
    st.subheader("About")
    lines = [
        "Every Scooby knows the importance of quality research tools.",
        "Whether you need a list of missing girls from the past 50 years or just want to know what kind of hotties your new boo used to be into, the value of finding the right tome or stack of newspapers can't be overstated.",
        "But this is 2022, so let's follow in the footsteps of one Jenny Calendar and get digital with it.",
    ]
    for line in lines:
        st.markdown(line)
    st.subheader("How to Use")
    lines = [
        "Type a word, phrase, or [regular expression](https://en.wikipedia.org/wiki/Regular_expression) into the search bar to view the number of times it appeared in each episode. "
        + "Then view the highlighted matches in the box below. "
        + "So just how many times HAS Jenny said the word 'noms'...?"
    ]
    for line in lines:
        st.markdown(line)


def display_line_prettily(
    row, pattern, show_line_nums: bool = True, quoting: bool = True
):
    COLOR = "BlueViolet"
    name = row["speaker"]
    line = row["line"]
    num = row["line_num"]
    line = re.sub(
        "(" + pattern + ")",
        f"<span style='color:{COLOR};font-weight:bold;'>" + r"\1" + "</span>",
        line,
        flags=re.IGNORECASE,
    )
    markdown = line if name == "NOTES" else f"**{name}:** {line}"
    if show_line_nums:
        markdown = f"({num}) " + markdown
    if quoting:
        markdown = "> " + markdown
    return markdown


def page_dataframe(df, page_size: int = 10):
    num_pages = math.ceil(len(df) / page_size)
    if num_pages <= 1:
        return df
    page_num = st.number_input("Page", min_value=0, max_value=num_pages)
    min_line, max_line = page_size * page_num, page_size * (page_num + 1)
    max_line = min(max_line, len(df))
    page = df.iloc[min_line:max_line, :]
    return page


def display_df_prettily(
    df,
    pattern,
):
    show_context = st.checkbox("Show Context", value=False)
    if not show_context:
        df = df[df["count"] > 0]
    page = page_dataframe(df)
    show_line_nums = st.checkbox("Show Line Numbers", value=True)
    pretty_lines = [
        display_line_prettily(row, pattern, show_line_nums=show_line_nums)
        for idx, row in page.iterrows()
    ]
    md = "\n\n".join(pretty_lines)
    st.markdown(md, unsafe_allow_html=True)


def search_widget(df):
    df = df.copy()
    shows = ["Buffering the Vampire Slayer", "Angel On Top"]
    pattern = st.text_input(
        "Search Pattern",
        value=r" noms",
        help="Search for a word, phrase, or regular expression",
    )
    with st.sidebar:
        st.header("Search Settings")
        ignore_case = st.checkbox("Ignore Case", value=True)
        filter_shows = st.multiselect("Shows", options=shows, default=shows)
    flags = re.IGNORECASE if ignore_case else 0
    show_df = df[df["show"].isin(filter_shows)]
    df["count"] = show_df["line"].apply(
        lambda x: len(re.findall(pattern, str(x), flags=flags))
    )
    return df, pattern


def graph_it(df):
    st.bar_chart(data=df, x="episode_date", y="count")


def show_results_by_episode(df, pattern):
    df["header"] = df["ep_id"] + ": " + df["title"]
    counts = df.groupby("header").sum("count")
    matching_eps = counts[counts["count"] > 0].index
    with st.expander("Matches", expanded=True):
        header_selected = st.selectbox(
            "Episode",
            options=matching_eps,
            format_func=lambda s: f"{s} ({counts['count'][s]})",
        )
        matches = df[df["header"] == header_selected]
        display_df_prettily(matches, pattern)


def main():
    st.title("The Library")
    about()
    st.header("Search")
    df = dataframe.create_full_dataframe()
    count_df, pattern = search_widget(df)
    grouped = count_df.groupby(["episode_date", "speaker"])["count"].sum().reset_index()
    graph_it(grouped)
    show_results_by_episode(count_df, pattern)


if __name__ == "__main__":
    main()
