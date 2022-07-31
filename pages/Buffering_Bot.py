import streamlit as st

from podbot.chatbot import (
    PodBot,
    get_trained_host_bot,
)

state = st.session_state


def format_probability(pair):
    token, prob = pair
    quotes = False
    include_prob = True
    label = f"'{token}'" if quotes else str(token)
    if include_prob:
        str_len = 20
        padding = str_len - len(label)
        label += " " * padding + f"({prob:.2f}%)"
    return label


def format_line(speaker_bot, sentence):
    line = f">**{speaker_bot.name}:** {sentence}"
    return line


def add_word(speaker_bot, new_token):
    speaker_bot.add_token(new_token)


def random_sentence(speaker_bot):
    rando = st.button("Randomize")
    if "line" not in state or rando:
        state["line"] = speaker_bot.speak()
    return state["line"]


def add_random_token(speaker_bot):
    speaker_bot.bot.generate_random_token()


def finish_sentence(speaker_bot):
    speaker_bot.bot.generate_chain()


def add_to_transcript(speaker_bot, formatted_line):
    state["lines"].append(formatted_line)
    speaker_bot.bot.tokens = []


def unified_display():
    if "lines" not in state:
        state["lines"] = []

    hosts = ["Jenny", "Kristin", "LaToya", "Morgan", "Mack", "Alba"]

    cols = st.columns(3)
    with cols[0]:
        speaker = st.selectbox("Speaker", options=hosts)

    # Train or retrieve hostbot
    if speaker not in state:
        speaker_bot = get_trained_host_bot(speaker)
        state[speaker] = speaker_bot
    speaker_bot = state[speaker]

    next_probs = [
        (token, prob)
        for (token, prob) in speaker_bot.bot.next_word_probabilities()
        if token is not None
    ]
    with cols[1]:
        new_token = st.selectbox(
            "Next Word",
            options=next_probs,
            format_func=format_probability,
            help="Type to filter",
        )
        print("Options", next_probs)
        print("New token", new_token)
        if new_token is not None:
            new_token = new_token[0]

    cols = st.columns(4)
    with cols[0]:
        st.button("Add Word", on_click=add_word, args=[speaker_bot, new_token])
    with cols[1]:
        st.button("Add Random Word", on_click=add_random_token, args=[speaker_bot])
    with cols[2]:
        st.button("Finish Sentence", on_click=finish_sentence, args=[speaker_bot])

    line = PodBot.format_sentence(speaker_bot.bot.tokens)
    formatted_line = format_line(speaker_bot, line)
    st.markdown(formatted_line)
    st.button(
        "Add to Transcript",
        on_click=add_to_transcript,
        args=[speaker_bot, formatted_line],
    )
    transcript = "  \n\n".join(state["lines"])
    return transcript


def main():

    st.write("# Buffering Bot")

    st.info(
        "Have you ever wanted to write an episode of BTVS without having to "
        + "think of what to say or worry about making sense? Look no further!"
    )
    exp = st.expander("Transcript", expanded=True)
    transcript = unified_display()
    with exp:
        st.markdown(transcript)


main()
