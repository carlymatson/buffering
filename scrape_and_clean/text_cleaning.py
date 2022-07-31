import re
from collections import Counter
from pathlib import Path
from pprint import pprint

CHARACTER_REMAPS = {
    "Æ": "E",
    "à": "a",
    "ä": "a",
    "á": "a",
    "é": "e",
    "ë": "e",
    "è": "e",
    "í": "i",
    "ī": "i",
    "ö": "o",
    "ō": "o",
    "ü": "u",
    "û": "u",
    "ʊ": "u",
    "ñ": "n",
    "ʌ": "u",
    "ʃ": "sh",
    "\.{3,}": "… ",
    "\u2018": "'",  # ‘
    "\u2019": "'",  # ’
    "\u02d0": " ",  # ː
    "\u2060": " ",  # "word joiner"
    chr(8211): "-",
    chr(8212): "-",
    "“": '"',
    "”": '"',
    "\xa0": " ",
    # "\u200b": " ",
    "\s*\n\s*": "\n",
}

KRISTIN_SPELLINGS = [
    "Kistin",
    "Krisin",
    "Kirstin",
    "Kristen",
    "Krirstin",
    "Kristine",
    "Krisitn",
    "Krstin",
    "Kritin",
    "Kristn",
]

NAME_REMAPS = {
    "Jeny": "Jenny",
    "Jennie": "Jenny",
    "Rishi": "Hrishi",
    "Riishi": "Hrishi",
    "Brittani": "Brittany",
    **{s: "Kristin" for s in KRISTIN_SPELLINGS},
}


def perform_remaps(text, remaps):
    for old, new in remaps.items():
        text = re.sub(old, new, text)
    return text


def strip_spacing_before_punctuation(text):
    text = re.sub(" ([,.?!:])", "\1", text)
    return text


def clean_characters(text):
    text = perform_remaps(text, CHARACTER_REMAPS)
    text = strip_spacing_before_punctuation(text)
    text = re.sub(" {2,}", " ", text)
    return text


def clean_speakers(text):
    text = perform_remaps(text, NAME_REMAPS)
    return text


# FIXME The next two functions are similar and maybe should be combined
def clean_lines(text):
    remaps = {
        "([a-z])(Jenny|Kristin):": r"\1\n\2:",
        "\n([a-z])": r"\1",
    }
    text = perform_remaps(text, remaps)
    return text


def merge_run_ons(text: str) -> str:
    # Insert note attributions
    text = re.sub("\n(\\[.+?\\])\n", r"\nNOTES: \1\n", text, re.DOTALL)
    # Merge lines
    text = re.sub("\n^([^:\n]+)$", r" \1", text, flags=re.MULTILINE)
    # Remove note attributions
    text = re.sub("Notes:", "", text)
    return text


def clean_transcript(text):
    text = clean_characters(text)
    text = clean_speakers(text)
    text = merge_run_ons(text)
    text = clean_lines(text)
    return text.strip("\n")


### Counts ###


def count_characters(text):
    # More edits to make:
    # Remove spaces before colons
    char_counts = Counter(text)
    lowercase = [chr(ord("a") + i) for i in range(26)]
    uppercase = [chr(ord("A") + i) for i in range(26)]
    pprint(
        {
            c: (ord(c), count)
            for c, count in char_counts.items()
            if c not in lowercase + uppercase
        }
    )


def count_speakers(text):
    pattern = "^[a-zA-Z]+:"
    speakers = re.findall(pattern, text, flags=re.MULTILINE)
    pprint(Counter(speakers))


def count_speakers(text):
    pattern = "^[a-zA-Z]+:"
    speakers = re.findall(pattern, text, flags=re.MULTILINE)
    pprint(Counter(speakers))


def write_cleaned_transcripts(transcripts):
    cleaned_dir = Path("./cleaned")
    for file, transcript in transcripts.items():
        text = clean_transcript(transcript)
        filepath = cleaned_dir / f"{file}.txt"
        with open(filepath, "w") as f:
            f.write(text)


def experiment_with_parsing(transcripts):
    all = "\n".join(transcripts.values())
    text = clean_transcript(all)
    count_characters(text)
    count_speakers(text)
    # check_parsing(text)
