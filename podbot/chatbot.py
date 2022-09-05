import re
from typing import List, Iterable
from pathlib import Path

from analysis import data_utils
from podbot.markov import MarkovBot


class PodBot:
    def __init__(self, name):
        self.bot = MarkovBot()
        self.name = name

    @staticmethod
    def clean(line: str) -> str:
        line = re.sub('"', "", line)  # Remove quotes
        return line

    @staticmethod
    def format_sentence(tokens: Iterable[str]) -> str:
        tokens = [token for token in tokens if token is not None]
        line = " ".join(tokens)
        line = strip_spacing_before_punctuation(line)
        return line

    @staticmethod
    def tokenize_text(text: str) -> List[str]:
        text = space_out_punctuation(text)
        corpus_words = [word for word in text.split(" ") if word != ""]
        return corpus_words


    def train(self, *lines):
        for line in lines:
            line = PodBot.clean(line)
            chain = self.tokenize_text(line)
            self.bot.train(chain)

    def add_token(self, token: str) -> None:
        self.bot.tokens.append(token)

    def speak(self, min_length=10):
        chain = self.bot.generate_chain(min_length=min_length)
        line = PodBot.format_sentence(chain)
        return line

    def __hash__(self):
        return self.name

# Podcast-specific cleaning and tokenization
def space_out_punctuation(text: str) -> str:
    text = text.replace("\n", " ")
    punctuation = ",.?!-():" + '"'
    for mark in punctuation:
        text = text.replace(mark, f" {mark} ")
    return text


def strip_spacing_before_punctuation(text: str) -> str:
    punc = ",.?!:"
    for char in punc:
        text = text.replace(" " + char, char)
    return text



def get_trained_host_bot(name: str) -> PodBot:
    bot = PodBot(name=name)
    lines = [
        line for fp in data_utils.TRANSCRIPT_DIR.iterdir() 
        for line in data_utils.get_dialogue(data_utils.read_transcript(fp), speaker=name)
    ]
    bot.train(*lines)
    return bot
