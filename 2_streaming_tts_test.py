import os, sys, asyncio, tempfile, subprocess
from dotenv import load_dotenv
from openai import AsyncOpenAI

async def speak_line(client, text):
    text = text.strip()
    if not text:
        return
    with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as tmp:
        path = tmp.name
    print(f"  -> requesting TTS for: {text!r}")
    try:
        async with client.audio.speech.with_streaming_response.create(
            model="gpt-4o-mini-tts",
            voice="alloy",
            input=text
        ) as resp:
            await resp.stream_to_file(path)
        print(f"  -> saved chunk: {path}")
        try:
            subprocess.run(["afplay", path], check=False)
        except Exception as e:
            print(f"  -> afplay not available or failed: {e}")
    finally:
        try:
            os.remove(path)
        except OSError:
            pass

async def main(txt_path):
    print("loading .env …")
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    print("have_key =", bool(api_key))
    if not api_key:
        raise SystemExit("Missing OPENAI_API_KEY in .env")
    client = AsyncOpenAI(api_key=api_key)
    if not os.path.exists(txt_path):
        raise SystemExit(f"File not found: {txt_path}")
    with open(txt_path, "r", encoding="utf-8") as f:
        lines = [ln.strip() for ln in f if ln.strip()]
    print(f"lines to speak: {len(lines)}")
    for i, line in enumerate(lines, 1):
        print(f"[{i}/{len(lines)}]")
        await speak_line(client, line)
    print("done.")

if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else "narration.txt"
    try:
        asyncio.run(main(path))
    except KeyboardInterrupt:
        print("\n^C — stopped by user")
