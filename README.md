# Buffering the Vampire Slayer Podcast Project

## Overview

This project is a data scientist's ode to Buffering the Vampire Slayer and Angel on Top! I used the public transcripts to do a recreational project including such tasks as tracking jingle usage, counting how many times Jenny said "wow wow wow", and even a text-generating BufferingBot!

## Sections
- View the frequency of word and phrase usage over time. Also jingles!
- View highlighted matches within context (bonus feature)
- Look at a timeline of significant events.
- Generate text using podcast host bots!

## Running the Project Locally

The visualization libraries used in this project involve a lot of dependencies, so you should install them in a virtual environment. Execute the commands below in a terminal session to do so.
```
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```
Now to run the project, simply execute 
```
streamlit run main.py
```

To-do
- Implement Streamlit pages
- Implement BufferingBot
