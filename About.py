import streamlit as st

from analysis import dataframe

st.set_page_config(layout="centered")
st.markdown("# A Celebration of Buffering the Vampire Slayer")


def welcome():
    st.header("Welcome, Gentle Viewers...")
    about_lines = [
        # "Welcome gentle viewers!",
        "You find before you a hodgepodge of projects which were completed with the episode transcripts, a moderate knowledge of coding, and too much free time.",
        "*Look back over a history of the podcast!*",
        "*Talk like LaToya!*",
        "*Finally figure out how many times Jenny has said \"slots\" and \"noms\"!*",
        "All these delights and more await you on our journey...",
    ]
    for line in about_lines:
        st.markdown(line)
    # st.write(about)


def relevant_quote():
    st.subheader("A Relevant Excerpt")
    st.markdown(
        "While making this project I was lucky enough to stumble upon a relevant exchange from an earlier episode.\n\n "
        + "*From Season 3 Episode 8: Lovers Walk, while discussing a singing stuffed bat...*"
    )
    quote_lines = [
        ">**Jenny:** Perhaps the key to gift giving when it comes to me, is just whatever it is, make sure my voice is inside of it.",
        ">**Kristin:** Oh my god. You just set yourself a trap for life. We're gonna have a room full of things that just say your voice now.  ",
        ">**Joanna:** So when I get you like a witch PEZ, when you open its jaw—",
        ">**Jenny:** It better sing.",
    ]
    st.markdown("\n\n".join(quote_lines))
    # for line in quote_lines:
    # st.markdown(">" + line)


def show_sources():
    ### Sources
    st.subheader("Sources")
    lines = [
        "All transcript data was obtained from the BTVS website at https://www.bufferingthevampireslayer.com/transcriptions.",
        "Air dates were gathered from https://www.stitcher.com/show/buffering-the-vampire-slayer.",
        "The source code for this project is available at https://github.com/carlymatson/buffering.",
    ]

    for line in lines:
        st.write(line)

    st.warning("Disclaimer: I could only find transcripts for Season 3 of Angel on Top, so Brittany Ashley and Laura Zak are tragically absent. We will remember them in our hearts.")


welcome()
relevant_quote()
show_sources()
