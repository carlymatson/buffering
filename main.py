import sys
from pathlib import Path
from pprint import pprint
from scrape_and_clean import episode_info, read_pdf

from scrape_and_clean import text_cleaning
import podbot.chatbot as chatbot

PDF_DIR = Path("./episodes")
CONVERTED_DIR = Path("./converted")
CLEANED_DIR = Path("./cleaned")


def read_text(filename: str) -> str:
    with open(filename, "r") as f:
        text = f.read()
    return text


def get_directory_contents(dir, get_contents=read_text):
    transcripts = {file.stem: get_contents(file) for file in dir.iterdir()}
    return transcripts


def write_files(transcripts, dir):
    for file, transcript in transcripts.items():
        text = text_cleaning.clean_transcript(transcript)
        filepath = dir / f"{file}.txt"
        with open(filepath, "w") as f:
            f.write(text)


def play_with_bots():
    # Do additional parsing - remove notes and URLs, maybe other stuff too
    # Get lines for particular characters
    # Tokenize text
    # Train Markov bot
    pass


def adhoc(text):
    ep, remnants = episode_info.parse_episode(text)
    print(ep.show)
    print(ep.episode)
    pprint(ep.lines[:5])
    print(f"Length of remnants: {len(remnants)}")


def train_on_episode(bot, episode):
    speakers_lines = [line for speaker, line in episode.lines if speaker == bot.name]
    for line in speakers_lines:
        bot.train(line)


def main():
    # Scrape PDFs
    # pdfs = get_directory_contents(PDF_DIR, get_contents=pdf.get_pdf_text)
    # write_files(pdfs, CONVERTED_DIR)
    transcripts = get_directory_contents(CONVERTED_DIR)
    cleaned = {
        file: text_cleaning.clean_transcript(text) for file, text in transcripts.items()
    }
    # write_files(cleaned, CLEANED_DIR)
    eps = {
        ep_stem: episode_info.parse_episode(text) for ep_stem, text in cleaned.items()
    }
    jenny_bot = chatbot.PodBot("Jenny")
    kristin_bot = chatbot.PodBot("Kristin")
    ep, remnants = eps["ep_159"]
    for (ep, remnants) in eps.values():
        train_on_episode(jenny_bot, ep)
        train_on_episode(kristin_bot, ep)
    for i in range(5):
        jenny_bot.speak()
        kristin_bot.speak()
    return

    if len(sys.argv) > 1:
        ep_nums = [int(n) for n in sys.argv[1:]]
        for ep_num in ep_nums:
            filestem = f"ep_{ep_num:03}"
            text = cleaned[filestem]
            adhoc(text)
            print("-" * 30)


if __name__ == "__main__":
    main()
