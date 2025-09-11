#!/usr/bin/env bash
set -euo pipefail

# Load your API key from .env (kept local/ignored)
source .env

# Generate the MP3
rm -f hello.mp3
curl -sS --fail-with-body -o hello.mp3 -X POST https://api.openai.com/v1/audio/speech \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model":"gpt-4o-mini-tts","voice":"alloy","input":"My name is Kenza and this is my answer to question 2.","format":"mp3"}'

# Play on macOS if available
command -v afplay >/dev/null && afplay hello.mp3 || true
