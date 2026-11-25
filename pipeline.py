import json
import time

from faster_whisper import WhisperModel
from google import genai

MODEL_NAME = "gemini-3.5-flash-lite"

RUBRIC_PROMPT = """
You are a call quality checker. Read this customer service call and reply with ONLY a JSON object, no other words, with these keys:
- politeness: a number from 1 to 5
- issue_resolved: true or false
- reason: one short sentence explaining your scores

Call:
{call_text}
"""

_whisper = None


def transcribe(audio_path):
    """Turn an audio file into text."""
    global _whisper
    if _whisper is None:
        _whisper = WhisperModel("small", device="cpu", compute_type="int8")
    segments, _info = _whisper.transcribe(audio_path)
    return " ".join(segment.text.strip() for segment in segments)


def score_call(call_text, api_key, tries=5):
    """Score a call transcript. Retries if Gemini is busy."""
    client = genai.Client(api_key=api_key)
    for attempt in range(tries):
        try:
            reply = client.models.generate_content(
                model=MODEL_NAME,
                contents=RUBRIC_PROMPT.format(call_text=call_text),
            )
            cleaned = reply.text.replace("```json", "").replace("```", "").strip()
            return json.loads(cleaned)
        except Exception:
            time.sleep(5)
    raise RuntimeError("Gave up after several tries")


def analyze(audio_path, api_key):
    """The whole pipeline: audio in, transcript and scores out."""
    transcript = transcribe(audio_path)
    scores = score_call(transcript, api_key)
    return transcript, scores
