import streamlit as st

from podbot.chatbot import (
    PodBot,
    get_trained_host_bot,
)

st.set_page_config(layout="centered")
state = st.session_state


def initialize_state():
    #values = {"speaker_name": "Jenny", "next_word": "Hello", "lines": []}
    values = {"speaker_name": "Jenny", "lines": []}
    for key, value in values.items():
        if key not in state:
            print(f"initializing state {key}={value}")
            state[key] = value


@st.cache(allow_output_mutation=True)
def get_bot(speaker: str) -> PodBot:
    return get_trained_host_bot(speaker)


def about():
    #st.subheader("About")
    lines = [
        "Have you ever noticed how auto-correct picks up on your speech patterns? Ever wished you could just have it talk for you?",
        "Well now, with the power of [Markov chains](https://en.wikipedia.org/wiki/Markov_chain), we can predict what word you are likely to say next! You can use this to generate text that actually sounds like the speaker. So that you, too, can one day have as many podcasts as Joanna Robinson.",
    ]
    for line in lines:
        st.markdown(line)

    with st.sidebar:
        st.subheader("How to Use")
        lines = [
            "**Selecting a Word:** Use the drop down menu to select the next word or punctuation mark. Try typing in the drop down to filter the list of words - it can be hundreds long! The numbers indicate what percentage of the time that word would be likely to come next.",
            "**Adding to a Sentence:** Add to a sentence by selecting a word to add, adding a random word, or randomly completing the sentence.",
            "**Adding to the Transcript:** Click the button to add the current line to the transcript. Once you're happy with it, save that bad boy for a rainy day and clear to start a new one.",
        ]
        for line in lines:
            st.markdown(line)
    st.info(
        '**Fun fact:** Kristin, Jenny, and LaToya all start 11\% their sentences with the word "Yeah", and it is the most common starting word for every BTVS speaker featured here (excpet for Hrishi). Wild.'
    )


def format_probability(token, prob):
    quotes = False
    include_prob = True
    label = f"'{token}'" if quotes else str(token)
    if include_prob:
        str_len = 20
        padding = str_len - len(label)
        label += " " * padding + f"({prob * 100:.2f}%)"
    return label


def format_markdown_quote(speaker_bot, sentence):
    line = f">**{speaker_bot.name}:** {sentence}"
    return line


def add_word(speaker_bot, new_token):
    speaker_bot.add_token(new_token)


def add_random_token(speaker_bot):
    speaker_bot.bot.generate_random_token()


def finish_sentence(speaker_bot):
    speaker_bot.bot.generate_chain()


def add_to_transcript(speaker_bot, line):
    if line == "":
        return
    formatted_line = format_markdown_quote(speaker_bot, line)
    state["lines"].append(formatted_line)
    speaker_bot.bot.tokens = []

def clear_transcript():
    state["lines"] = []

def clear_line(speaker_bot):
    speaker_bot.bot.tokens = []

def unified_display():

    hosts = [
        "Jenny",
        "Kristin",
        "LaToya",
        "Morgan",
        "Mack",
        "Alba",
        "Ira",
        "Joanna",
        "Hrishi",
        "Gaby",
    ]

    cols = st.columns(3)
    with cols[0]:
        speaker = st.selectbox("Speaker", options=hosts, key="speaker_name")

    # Train or retrieve hostbot
    speaker_bot = get_bot(speaker)

    probs = speaker_bot.bot.next_word_probabilities()
    if list(probs.keys()) == [None]:
        probs = speaker_bot.bot.next_word_probabilities(token_pair=(None, None))
    non_null_probs = [key for key in probs.keys() if key is not None]
    next_token_options = sorted(non_null_probs, key=lambda x: -probs.get(x, 0))
    with cols[1]:
        new_token = st.selectbox(
            "Select Next Word",
            options=next_token_options,
            format_func=lambda x: format_probability(x, probs.get(x, 0)),
            help="Type to filter",
            key="next_word",
        )
        # if new_token is not None:
        # new_token = new_token[0]
    with cols[2]:
        st.write("")
        st.write("")
        st.button("Add to Line", on_click=add_word, args=[speaker_bot, new_token])

    cols = st.columns(4)
    cols[0].write("Add Randomly:")
    cols[1].button("One Word", on_click=add_random_token, args=[speaker_bot], help = "Add one randomly chosen word")
    cols[2].button("Finish Sentence", on_click=finish_sentence, args=[speaker_bot], help="Add random words until the line is complete")

    line = PodBot.format_sentence(speaker_bot.bot.tokens)
    formatted_line = format_markdown_quote(speaker_bot, line)
    cols = st.columns((6,1,1))
    cols[0].markdown(formatted_line)
    cols[1].button("Clear", on_click=clear_line, args=[speaker_bot], help="Clear line")
    cols[2].button(
        "Add",
        on_click=add_to_transcript,
        args=[speaker_bot, line],
        help="Add to transcript"
    )
    transcript = "  \n\n".join(state["lines"])
    return transcript


def main():
    initialize_state()

    st.title("BufferingBot")
    about()

    st.subheader("Text Generator")

    transcript = unified_display()
    exp = st.expander("Transcript", expanded=True)
    with exp:
        st.markdown(transcript)
        st.button("Clear Transcript", on_click=clear_transcript)
    # st.write(st.session_state)


main()
