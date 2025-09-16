Text-to-Speech Driver (what this script does):

3_voices_effects.py interactively creates an MP3 narration from your text.
When you run python 3_voices_effects.py, it:

Prompts you to choose a voice by number from:

alloy, 2) echo, 3) fable, 4) onyx, 5) nova, 6) shimmer, 7) coral, 8) verse, 9) ballad, 10) ash, 11) sage, 12) marin, 13) cedar.

Prompts you to choose an effect by number from:

neutral, 2) cheerful, 3) angry, 4) sad, 5) surprised, 6) whisper, 7) serious, 8) fast, 9) slow.

Asks you to type the message you want spoken.

Generates speech, plays it, and saves the result as an MP3 in voices_out/ with a timestamped filename (e.g., tts_ballad_cheerful_YYYYMMDD_HHMMSS.mp3).
