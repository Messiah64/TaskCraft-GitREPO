##Importing libraries
import os
import sys
import streamlit as st

# Importing functions
from utility.classes import dataProcessor
from audio_recorder_streamlit import audio_recorder

# Set up path to utility folder
absolute_path = os.path.join(os.path.dirname(__file__), 'utility')
sys.path.append(absolute_path)  # Add the absolute path to the system path

# Create Class instance
dataprocessor = dataProcessor()

dataprocessor.local_css()

st.title("Whisper App :studio_microphone: :clipboard: :calendar:")

st.markdown(
    """
    ##### Description:
    Record your daily tasks and have an AI Assistant narrow it down into, small accomplishable tasks for you. Your very own daily planner!
    """
)

st.divider()  # 👈 Draws a horizontal rule

audio_bytes = audio_recorder()
if audio_bytes:
    value = st.audio(audio_bytes, format="audio/wav")


with st.form("record_form"):
   # Every form must have a submit button.
    submitted = st.form_submit_button("Process")