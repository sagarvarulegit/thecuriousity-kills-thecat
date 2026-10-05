"""
Synthesize Episode 1 voiceovers using ElevenLabs API with Brian or George.
"""

import os
import requests
from dotenv import load_dotenv
from generate_audio import EPISODE_ACTS, SHORTS

load_dotenv()

ELEVEN_KEY = os.getenv("ELEVEN_LABS_API_KEY")
# Brian: nPczCjzI2devNBz1zQrb (Deep, Resonant) | George: JBFqnCBsd6RMkjVDRZzb (Warm Storyteller)
VOICE_ID = "nPczCjzI2devNBz1zQrb"  # Brian
MODEL_ID = "eleven_multilingual_v2"

HEADERS = {
    "xi-api-key": ELEVEN_KEY,
    "Content-Type": "application/json"
}

AUDIO_DIR = "ajanta-ellora/assets/episode-01/audio_elevenlabs"
os.makedirs(AUDIO_DIR, exist_ok=True)

def generate_tts(text: str, filename: str):
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"
    payload = {
        "text": text,
        "model_id": MODEL_ID,
        "voice_settings": {
            "stability": 0.50,
            "similarity_boost": 0.85,
            "style": 0.20,
            "use_speaker_boost": True
        }
    }
    
    print(f"Generating {filename} ({len(text)} chars)...")
    resp = requests.post(url, headers=HEADERS, json=payload)
    if resp.status_code == 200:
        out_path = os.path.join(AUDIO_DIR, filename)
        with open(out_path, "wb") as f:
            f.write(resp.content)
        print(f"  -> Saved {out_path}")
        return out_path
    else:
        print(f"  -> Error {resp.status_code}: {resp.text}")
        return None

def main():
    print(f"Starting ElevenLabs Narration Generation using Voice ID: {VOICE_ID} (Brian)...")
    
    # Generate Act 1 to 8
    for act in EPISODE_ACTS:
        fname = f"{act['act']}.mp3"
        generate_tts(act["text"], fname)
        
    # Generate Shorts
    for short in SHORTS:
        fname = f"{short['name']}.mp3"
        generate_tts(short["text"], fname)

    print("\nAll ElevenLabs voiceovers generated successfully!")

if __name__ == "__main__":
    main()
