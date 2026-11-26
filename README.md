# Voice Call QA Analyzer

A small tool that listens to a customer service call recording, transcribes it, and scores it for politeness and whether the issue was resolved.

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/user12345-cyber/voice-call-qa/blob/main/voice_qa_launcher.ipynb)


**Try it:** download one of the sample call recordings in this repository (the mp3 files), then upload it on the app page and click Analyze call. To run the app you need your own free Gemini API key, saved in Colab Secrets as GEMINI_API_KEY.
## How it works

1. **Transcribe**: faster-whisper turns the audio into text.
2. **Score**: Gemini reads the transcript and returns JSON with a politeness score (1-5), whether the issue was resolved, and a short reason.
3. **Display**: a Streamlit page lets you upload a recording and see the results.

## Results

I wrote 12 practice calls (including tricky ones like sarcasm and unclear endings), turned them into audio, and compared the pipeline's scores to my own hand labels.

- Issue resolved: agreed on 12 of 12 calls
- Politeness: agreed exactly on 8 of 12 calls (about 67%)

The biggest disagreements were a sarcastic call (I gave 3, the model gave 1) and a rushed but effective call (I gave 5, the model gave 2). The model seems to be stricter than me on sarcasm and curtness.

## Limitations

- Only 12 calls, labeled by one person (me), so the numbers are a rough guide.
- The calls are synthetic: written by an LLM and read by a single text-to-speech voice, so speaker labels are lost and real call noise is not tested.
- The politeness scale is subjective, and exact-match agreement is a strict measure.

## Run it

1. Install the tools: `pip install -r requirements.txt`
2. Set your Gemini API key: `export GEMINI_API_KEY=your_key_here`
3. Start the app: `streamlit run app.py`

Never commit your API key to the repository.

## Files

- `pipeline.py`: transcription and scoring logic
- `app.py`: the Streamlit upload page
- `requirements.txt`: dependencies
