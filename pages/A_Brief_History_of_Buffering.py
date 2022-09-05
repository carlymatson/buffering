import streamlit as st

from analysis.timelines import main

st.set_page_config(layout="wide")


def about():
    #st.subheader("About")
    lines = [
        ("We all know the real reason that people listen to the podcast - that sweet, sweet bonus content. " 
        + "Look back at some of the jingles and special episodes that came about through Jenny's musical prowess and, of course, Kristin's unparalleled natural talent."),
    ]
    for line in lines:
        st.markdown(line)


st.title("A Brief History of Buffering")
about()
main()
