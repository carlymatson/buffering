import json

import streamlit
from streamlit_timeline import timeline

with open("sample_timeline.json", "r") as f:
    data = json.load(f)

timeline(data, height=800)
