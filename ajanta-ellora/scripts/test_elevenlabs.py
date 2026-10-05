import os
import requests
from dotenv import load_dotenv

load_dotenv()
headers = {"xi-api-key": os.getenv("ELEVEN_LABS_API_KEY")}
resp = requests.get("https://api.elevenlabs.io/v1/voices", headers=headers)
voices = resp.json().get("voices", [])

print("Top Storyteller / Documentary Voices in ElevenLabs Account:")
for v in voices:
    labels = v.get("labels", {})
    name = v["name"]
    vid = v["voice_id"]
    accent = labels.get("accent", "")
    desc = labels.get("description", "")
    use = labels.get("use case", "")
    if any(k in f"{name} {desc} {use}".lower() for k in ["story", "narrat", "docu", "deep", "george", "adam", "brian", "charlie"]):
        print(f"- {name} (ID: {vid}) | Accent: {accent} | Style: {desc} | Use: {use}")
