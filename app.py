import os
import tempfile

import streamlit as st

import pipeline

st.title("Voice Call QA Analyzer")
st.write("Upload a customer service call recording and get a quality score.")

api_key = os.environ.get("GEMINI_API_KEY", "")
if not api_key:
    api_key = st.text_input("Gemini API key", type="password")

uploaded = st.file_uploader("Call recording", type=["mp3", "wav", "m4a", "flac"])

if uploaded and api_key and st.button("Analyze call"):
    suffix = os.path.splitext(uploaded.name)[1]
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp.write(uploaded.read())
        audio_path = tmp.name

    with st.spinner("Listening and scoring..."):
        transcript, scores = pipeline.analyze(audio_path, api_key)

    st.subheader("Scores")
    st.write("**Politeness (1-5):** " + str(scores["politeness"]))
    st.write("**Issue resolved:** " + ("Yes" if scores["issue_resolved"] else "No"))
    st.write("**Reason:** " + scores["reason"])

    st.subheader("Transcript")
    st.write(transcript)
