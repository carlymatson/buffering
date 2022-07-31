import streamlit as st

from analysis import dataframe

st.set_page_config(layout="wide")
st.markdown("# A Buffering Retrospective")


st.header("About")
about = "This project is a data-scientist's ode to the podcast Buffering the Vampire Slayer. It includes a chat-generating 'Buffering Bot' and a timeline of significant events. Basically I just wanted to play around with transcripts."
st.write(about)

st.header("Sources")
st.write(
    "All transcript data was obtained from the BTVS website at https://www.bufferingthevampireslayer.com/transcriptions."
)
st.write(
    "Air dates were gathered from https://www.stitcher.com/show/buffering-the-vampire-slayer."
)
st.write(
    "The source code for this project is available at https://github.com/carlymatson/buffering."
)
