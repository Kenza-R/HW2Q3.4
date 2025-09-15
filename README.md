# Intro to AI Applications — Homework 2

## Environment
- OS: macOS 15.4.1 (arm64)
- Git: git version 2.39.5 (Apple Git-154)
- Python: Python 3.13.7
- Shell: /bin/zsh

## Steps to reproduce
1. cd ~/Desktop/introai_hw2
2. git init
3. Create README.md 
4. git add README.md
5. git commit -m "init"

## Create a secrets file .env (kept local/ignored)
# ONE line only; no quotes/spaces around the key
printf "OPENAI_API_KEY=sk-...your_key..." > .env

## Ignore secrets (and later, the local Python venv)
printf ".env\nenv/\n" >> .gitignore
git add .gitignore
git commit -m "Ignore .env and local venv"
git push
## Quick TTS smoke test (shell script)
cat > 0_tts_test.sh <<'EOF'
#!/usr/bin/env bash
set -euo pipefail

# load API key
source .env

# generate mp3
rm -f hello.mp3
curl -sS --fail-with-body -o hello.mp3 -X POST https://api.openai.com/v1/audio/speech \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model":"gpt-4o-mini-tts",
    "voice":"alloy",
    "input":"My name is Kenza and this is my answer to question 2.",
    "format":"mp3"
  }'

# auto-play on macOS if available
command -v afplay >/dev/null && afplay hello.mp3 || true
EOF

chmod +x 0_tts_test.sh

## Create and activate a local Python virtual environment
python3 -m venv env
source env/bin/activate      # (you should see (env) in the prompt)

## Install required packages
python -m pip install --upgrade pip
python -m pip install --upgrade openai "openai[voice_helpers]" sounddevice numpy python-dotenv

## Tell VS Code to use this venv
Command Palette → Python: Select Interpreter → choose the interpreter inside introai_hw2/env.

## Streaming TTS test (Python)
# 1_streaming_tts_test.py
import os, shutil, subprocess
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()  # loads OPENAI_API_KEY from .env
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
  raise SystemExit("Missing OPENAI_API_KEY in .env")

client = OpenAI(api_key=api_key)

TEXT = "My name is Kenza and this is my answer to question 2."
OUT  = "tts_stream.mp3"

print("Requesting streaming TTS…")
with client.audio.speech.with_streaming_response.create(
    model="gpt-4o-mini-tts",
    voice="alloy",
    input=TEXT,
    format="mp3",
) as resp:
    resp.stream_to_file(OUT)

print(f"Saved: {OUT}")

# Optional auto-play on macOS
if shutil.which("afplay"):
    try:
        subprocess.run(["afplay", OUT], check=False)
    except Exception:
        pass
