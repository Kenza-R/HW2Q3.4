# ---- env check block (safe, non-secret) ----
import os, sys, hashlib
from dotenv import load_dotenv

def _check_env_only():
    loaded = load_dotenv()  # reads .env in this folder
    key = os.getenv("OPENAI_API_KEY", "")

    print("dotenv loaded:", loaded)
    print("key present:", bool(key))
    print("looks like OpenAI key prefix:", key.startswith(("sk-", "sk-proj-")))
    print("length:", len(key))
    # Safe fingerprint (non-reversible) to prove key loaded, without leaking it
    print("sha256(key) first 8:", hashlib.sha256(key.encode()).hexdigest()[:8] if key else "n/a")

if __name__ == "__main__" and "--check-env" in sys.argv:
    _check_env_only()
    sys.exit(0)
# ---- end env check block ----

# 1_streaming_tts_test.py
import os
import shutil
import subprocess
from dotenv import load_dotenv
from openai import OpenAI

# Load OPENAI_API_KEY from .env
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise SystemExit("Missing OPENAI_API_KEY in .env")

client = OpenAI(api_key=api_key)

TEXT = "My name is Kenza and this is my answer to question 2."
OUT = "tts_stream.mp3"

print("Requesting streaming TTS…")
with client.audio.speech.with_streaming_response.create(
    model="gpt-4o-mini-tts",
    voice="alloy",
    input=TEXT,
    format="mp3",
) as resp:
    resp.stream_to_file(OUT)

print(f"Saved: {OUT}")

# Optional: auto-play on macOS
if shutil.which("afplay"):
    try:
        subprocess.run(["afplay", OUT], check=False)
    except Exception:
        pass
