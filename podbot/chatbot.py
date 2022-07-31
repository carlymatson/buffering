import re
from typing import List, Iterable
from pathlib import Path

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

    def train(self, *lines):
        for line in lines:
            line = PodBot.clean(line)
            chain = tokenize_text(line)
            self.bot.train(chain)

    def add_token(self, token: str) -> None:
        self.bot.tokens.append(token)

    def speak(self, min_length=10):
        chain = self.bot.generate_chain(min_length=min_length)
        line = PodBot.format_sentence(chain)
        return line


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


def tokenize_text(text: str) -> List[str]:
    text = space_out_punctuation(text)
    corpus_words = [word for word in text.split(" ") if word != ""]
    return corpus_words


def get_transcript_lines(filepath, name):
    with filepath.open("r") as f:
        text = f.read()
    pattern = f"^{name}: (.*)$"
    lines = re.findall(pattern, text, flags=re.MULTILINE)
    return lines


def get_all_speaker_lines(name: str) -> List[str]:
    transcript_dir = Path("data/cleaned")
    all_lines = []
    for filepath in transcript_dir.iterdir():
        lines = get_transcript_lines(filepath, name)
        all_lines.extend(lines)
    return all_lines


def get_trained_host_bot(name: str) -> PodBot:
    bot = PodBot(name=name)
    lines = get_all_speaker_lines(name)
    bot.train(*lines)
    return bot
