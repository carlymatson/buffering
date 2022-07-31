import re

# FIXME Where is "title"?


class Episode:
    def __init__(self, transcript, show, episode, lines, notes):
        self.transcript = transcript
        self.show = show
        self.episode = episode
        self.lines = lines
        self.notes = notes


def extract_and_remove(text, pattern, only_one: bool = False):
    if only_one:
        m = re.search(pattern, text, flags=re.MULTILINE)
        extracted = m if m is None else m.group()
    else:
        extracted = re.findall(pattern, text, flags=re.MULTILINE)
    stripped = re.sub(pattern, "", text, flags=re.MULTILINE)
    reduced = re.sub(" {2,}", " ", stripped)
    reduced = re.sub("\n{2,}", "\n", reduced)
    return extracted, reduced


def parse_episode(text):
    transcript = text
    show_header_pattern = "^(Angel On Top|Buffering the Vampire Slayer)$"
    episode_headers = "^Episode \d[.:]\d+(?:\.\d+)?: .*$"
    note_pattern = "^\[.*\]$"
    line_pattern = "^([A-Z][a-zA-Z]+): (.*)$"
    show, text = extract_and_remove(text, show_header_pattern, only_one=True)
    episode, text = extract_and_remove(text, episode_headers, only_one=True)
    notes, text = extract_and_remove(text, note_pattern)
    lines, text = extract_and_remove(text, line_pattern)
    return Episode(transcript, show, episode, lines, notes), text.strip()


def convert_to_snake_case(s):
    underscored = re.sub("[- ]", "_", s)
    dedoubled = re.sub("_{2,}", "_", underscored)
    lower = dedoubled.lower()
    cleaned = re.sub("[^a-z0-9_]", "", lower)
    return cleaned


def format_episode_filename(episode):
    prefix = "buffy" if episode.show.startswith("B") else "angel"
    snake_title = convert_to_snake_case(episode.title)
    season = episode.season
    num = episode.number
    filename = f"{prefix}_{season}_{num:02}_{snake_title}.txt"
    return filename
