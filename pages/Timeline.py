import streamlit as st

from analysis.timelines import main

st.markdown("# A Brief History of Buffering")
options = ["Special Episodes", "Jingle Debuts"]
st.sidebar.multiselect("Timelines to Display", options=options)
main()
