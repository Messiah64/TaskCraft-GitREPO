import streamlit as st
import whisper

st.title("Whisper App")

# upload audio
audio_file = st.file_uploader("Upload audio", type=['wav', 'mp3', 'm4a'])

model = whisper.load_model("base")
st.text("Model Loaded")


if st.sidebar.button("Transcribe Audio"): 
    if audio_file is not None:
        st.sidebar.success("Generating Transcript")
        transcription = model.transcribe(audio_file.name)
        st.sidebar.success("Transcript generated successfully")
        st.text(transcription["text"])
    else: 
        st.sidebar.error("Please upload an audio file")
