import os, sys
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

text = "My name is Kenza and this is my answer to question 3."
if len(sys.argv) > 1:
    text = " ".join(sys.argv[1:])

out = "tts_python.mp3"
with client.audio.speech.with_streaming_response.create(
    model="gpt-4o-mini-tts",
    voice="alloy",
    input=text,
) as resp:
    resp.stream_to_file(out)
print(out)
