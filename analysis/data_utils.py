import re
from pathlib import Path
from typing import List

DATA_DIR = Path("data")
TRANSCRIPT_DIR = Path("data") / "cleaned5"

def read_transcript(filepath):
    with open(filepath, "r") as f:
        text = f.read()
    return text


def get_dialogue(text, speaker: str = None) -> List[str]:
    name = speaker or ".*?"
    pattern = f"^{name}: (.*)$"
    lines = re.findall(pattern, text, flags=re.MULTILINE)
    return lines