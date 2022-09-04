import streamlit as st

from analysis.timelines import main

st.set_page_config(layout="wide")


def about():
    st.header("About")
    lines = [
        "",
    ]
    for line in lines:
        st.markdown(line)


st.title("A Brief History of the Bufferingverse")
about()
st.header("Timeline")
main()
