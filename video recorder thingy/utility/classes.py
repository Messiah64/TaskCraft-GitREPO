##Import Extraction Libraries
import re
import streamlit as st

class dataProcessor:
    
    def __init__(self):
        # Initalize instance attributes
        self.file_name = r"C:\Users\Moham\OneDrive - dkip8171\Desktop\AI Projects\ClockHacks\video recorder thingy\docs\static\style.css"
        

    #CSS File For Streamlit Pages
    def local_css(self):
        with open(self.file_name) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
