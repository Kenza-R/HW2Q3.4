# 3_voices_effects.py
import os, sys, datetime, subprocess, time
from dotenv import load_dotenv
from openai import OpenAI, APITimeoutError

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise SystemExit("Missing OPENAI_API_KEY in .env")

# Increase default request timeout to 60s
client = OpenAI(api_key=api_key, timeout=60)

VOICES = ["alloy", "echo", "fable", "onyx", "nova", "shimmer", "coral", "verse", "ballad", "ash", "sage", "marin", "cedar"]
EFFECTS = ["neutral", "cheerful", "angry", "sad", "surprised", "whisper", "serious", "fast", "slow"]

def style_text(s: str, effect: str) -> str:
    t = s.strip()
    if effect == "neutral":   return t
    if effect == "cheerful":  return t.replace(".", "!") + "!"
    if effect == "angry":     return t.upper().rstrip(".!") + "!!"
    if effect == "sad":       return t.lower().replace(".", "...").replace("!", "...") + "..."
    if effect == "surprised": return t.rstrip(".!") + "?!"
    if effect == "whisper":   return (t.lower().rstrip(".!") + "…").replace(",", ", ")
    if effect == "serious":   return t.replace("!", ".")
    if effect == "fast":      return t.replace(", ", " ").replace("—", " ").replace(" - ", " ")
    if effect == "slow":      return t.replace(".", ",").replace("!", ",").replace("?", ",")
    return t

def choose(prompt: str, options: list[str]) -> str:
    for i, opt in enumerate(options, 1):
        print(f"{i}) {opt}")
    while True:
        sel = input(f"{prompt} [1-{len(options)}]: ").strip()
        if sel.isdigit() and 1 <= int(sel) <= len(options):
            return options[int(sel) - 1]
        print("Invalid choice, try again.")

def tts_to_file(voice: str, text: str, out: str, retries: int = 3) -> None:
    attempt = 0
    backoff = 2
    while True:
        attempt += 1
        try:
            with client.audio.speech.with_streaming_response.create(
                model="gpt-4o-mini-tts",
                voice=voice,
                input=text,
            ) as resp:
                resp.stream_to_file(out)
            return
        except APITimeoutError:
            if attempt >= retries:
                raise
            time.sleep(backoff)
            backoff *= 2  # exponential backoff
        except Exception:
            # transient network hiccup; retry a couple of times
            if attempt >= retries:
                raise
            time.sleep(backoff)
            backoff *= 2

def main():
    voice = choose("Select a voice", VOICES)
    effect = choose("Select an effect", EFFECTS)
    print()
    text = input("Enter the text to speak: ").strip()
    styled = style_text(text, effect)

    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    out = f"tts_{voice}_{effect}_{ts}.mp3"

    tts_to_file(voice=voice, text=styled, out=out)
    print(out)
    try:
        subprocess.run(["afplay", out], check=False)  # macOS auto-play
    except Exception:
        pass

if __name__ == "__main__":
    main()
