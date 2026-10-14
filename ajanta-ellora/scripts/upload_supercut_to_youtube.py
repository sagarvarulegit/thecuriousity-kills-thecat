#!/usr/bin/env python3
"""
YouTube Data API v3 Video & Metadata Uploader for Master Series Supercut
Channel: The Curiosity Kills The Cat
Automates:
  1. Resumable video upload (Full HD master 1080p, 58 mins, 1.85 GB)
  2. Custom thumbnail upload (16:9 Scale Contrast Variant A)
  3. Caption upload (Full English .srt subtitles, 540 cues)
  4. Complete SEO metadata (Title, Full Description with 55 chapters, Tags, Category: Education)
"""

import os
import sys
import time
import argparse
import http.client
import httplib2
from pathlib import Path

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

# Scopes required for upload, thumbnail, and captions
SCOPES = [
    "https://www.googleapis.com/auth/youtube.upload",
    "https://www.googleapis.com/auth/youtube.force-ssl",
    "https://www.googleapis.com/auth/youtube"
]

API_SERVICE_NAME = "youtube"
API_VERSION = "v3"

WORKSPACE_ROOT = Path(__file__).resolve().parent.parent.parent
SUPERCUT_DIR = WORKSPACE_ROOT / "ajanta-ellora" / "supercut"

DEFAULT_VIDEO_PATH = SUPERCUT_DIR / "final_videos" / "the_complete_megastructures_of_kailasa_and_ajanta_master_1080p.mp4"
DEFAULT_THUMBNAIL_PATH = SUPERCUT_DIR / "thumbnail" / "thumbnail_variant_a_scale_contrast.jpg"
DEFAULT_CAPTIONS_PATH = SUPERCUT_DIR / "subtitles" / "supercut_master.srt"
DEFAULT_CHAPTERS_PATH = SUPERCUT_DIR / "openmontage_bundle" / "metadata" / "chapters.txt"
DEFAULT_TOKEN_PATH = WORKSPACE_ROOT / "token.json"
DEFAULT_CLIENT_SECRETS = WORKSPACE_ROOT / "client_secret.json"

DEFAULT_TITLE = "The Impossible Subterranean Megastructures of Ancient India (Full Documentary)"

def load_description_with_chapters() -> str:
    chapters_text = ""
    if DEFAULT_CHAPTERS_PATH.exists():
        chapters_text = DEFAULT_CHAPTERS_PATH.read_text(encoding="utf-8").strip()
    
    desc = f"""Over 700 years before modern civil engineering, ancient Indian stonecutters achieved what modern geologists still struggle to explain: they excavated over 400,000 tons of solid volcanic basalt—not by building from the foundation up, but by carving directly downward from the mountain summit.

This complete, uninterrupted 7-part master documentary presents the full investigative arc of Kailasa Temple (Cave 16) and the mysterious crescent canyon of Ajanta. Remastered with theatrical broadcast audio (-14 LUFS) and continuous chapter navigation, this feature reveals the thermal shock quarrying mechanics, zero-tolerance astronomy, subterranean hydraulic defense networks, and acoustic resonance chambers that turned living rock into an architectural miracle.

TIMESTAMPS / CHAPTERS:
{chapters_text}

🔔 Subscribe to @thecuriousity-kills-thecat for deep-dive historical engineering documentaries.

#KailasaTemple #AjantaCaves #AncientEngineering #FullDocumentary #AncientIndia #ElloraCaves #Megaliths #HistoryDocumentary
"""
    return desc

DEFAULT_TAGS = [
    "Kailasa Temple",
    "Ajanta Caves",
    "Full Documentary",
    "Ancient Megastructures",
    "Ellora Caves",
    "How Kailasa Was Built",
    "Ancient Engineering",
    "Top Down Temple",
    "Rock Cut Architecture",
    "Ancient India",
    "Archaeology Documentary",
    "Ellora Cave 16",
    "Architect Kokasa",
    "Rashtrakuta Dynasty",
    "Vakataka Dynasty",
    "Ancient Technology",
    "Megaliths",
    "Indian History",
    "Ancient Builders",
    "Thermal Shock Quarrying",
    "Geotechnical Engineering",
    "Waghur River",
    "Ancient Mysteries",
    "Complete Series"
]

def get_authenticated_service(client_secrets_file: Path, token_file: Path):
    """Authenticate with YouTube Data API v3 using OAuth 2.0."""
    creds = None
    if token_file.exists():
        try:
            creds = Credentials.from_authorized_user_file(str(token_file), SCOPES)
            print(f"[AUTH] Loaded existing OAuth credentials from {token_file}")
        except Exception as e:
            print(f"[AUTH] Could not load token file: {e}")
            creds = None

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            print("[AUTH] Refreshing expired OAuth credentials...")
            creds.refresh(Request())
        else:
            if not client_secrets_file.exists():
                raise FileNotFoundError(
                    f"\n[ERROR] OAuth client secrets file not found: {client_secrets_file}\n"
                    "To upload via YouTube Data API v3:\n"
                    "1. Go to Google Cloud Console (https://console.cloud.google.com)\n"
                    "2. Enable 'YouTube Data API v3'\n"
                    "3. Create OAuth 2.0 Client ID (Application type: Desktop App)\n"
                    "4. Download JSON and save as 'client_secret.json' in project root.\n"
                )
            print(f"[AUTH] Starting OAuth 2.0 Web Authorization flow using {client_secrets_file}...")
            flow = InstalledAppFlow.from_client_secrets_file(str(client_secrets_file), SCOPES)
            creds = flow.run_local_server(port=0)

        with open(token_file, "w") as token:
            token.write(creds.to_json())
            print(f"[AUTH] Credentials saved to {token_file} for future uploads.")

    return build(API_SERVICE_NAME, API_VERSION, credentials=creds)

def upload_video(youtube, video_path: Path, title: str, description: str, tags: list, privacy_status: str, category_id: str = "27"):
    """Perform resumable video upload."""
    if not video_path.exists():
        raise FileNotFoundError(f"Video file not found at {video_path}")

    file_size_mb = os.path.getsize(video_path) / (1024 * 1024)
    print(f"\n[UPLOAD] Initiating upload for: {video_path.name} ({file_size_mb:.2f} MB)")
    print(f"[UPLOAD] Title: {title}")
    print(f"[UPLOAD] Privacy: {privacy_status} | Category ID: {category_id}")
    print(f"[UPLOAD] Tags count: {len(tags)}")

    body = {
        "snippet": {
            "title": title,
            "description": description,
            "tags": tags,
            "categoryId": category_id,
            "defaultLanguage": "en",
            "defaultAudioLanguage": "en"
        },
        "status": {
            "privacyStatus": privacy_status,
            "selfDeclaredMadeForKids": False
        }
    }

    # 16 MB chunk size for high-speed multi-megabyte supercut upload
    chunksize = 16 * 1024 * 1024
    media = MediaFileUpload(
        str(video_path),
        chunksize=chunksize,
        resumable=True,
        mimetype="video/mp4"
    )

    request = youtube.videos().insert(
        part=",".join(body.keys()),
        body=body,
        media_body=media
    )

    response = None
    retry_count = 0
    max_retries = 10

    print("[UPLOAD] Transferring chunks to YouTube servers...")
    while response is None:
        try:
            status, response = request.next_chunk()
            if status:
                progress = int(status.progress() * 100)
                uploaded_mb = (status.resumable_progress or 0) / (1024 * 1024)
                print(f"  -> Upload progress: {progress}% ({uploaded_mb:.1f} / {file_size_mb:.1f} MB)")
        except HttpError as e:
            if e.resp.status in [500, 502, 503, 504]:
                retry_count += 1
                if retry_count > max_retries:
                    raise e
                wait_time = 2 ** retry_count
                print(f"  [WARN] Retrying upload after HTTP {e.resp.status}. Waiting {wait_time}s...")
                time.sleep(wait_time)
            else:
                raise e

    video_id = response.get("id")
    print(f"\n[SUCCESS] Master Video uploaded successfully! Video ID: {video_id}")
    print(f"[SUCCESS] Video Watch URL: https://www.youtube.com/watch?v={video_id}")
    return video_id

def set_thumbnail(youtube, video_id: str, thumbnail_path: Path):
    if not thumbnail_path.exists():
        print(f"[THUMBNAIL] File not found: {thumbnail_path}. Skipping.")
        return
    print(f"\n[THUMBNAIL] Uploading 16:9 custom thumbnail: {thumbnail_path.name}")
    try:
        youtube.thumbnails().set(
            videoId=video_id,
            media_body=MediaFileUpload(str(thumbnail_path), mimetype="image/jpeg")
        ).execute()
        print("[THUMBNAIL] Successfully applied custom thumbnail!")
    except Exception as e:
        print(f"[THUMBNAIL ERROR] Could not set thumbnail: {e}")

def upload_captions(youtube, video_id: str, captions_path: Path):
    if not captions_path.exists():
        print(f"[CAPTIONS] File not found: {captions_path}. Skipping.")
        return
    print(f"\n[CAPTIONS] Uploading subtitle cue sheet: {captions_path.name}")
    try:
        youtube.captions().insert(
            part="snippet",
            body={
                "snippet": {
                    "videoId": video_id,
                    "language": "en",
                    "name": "English (Original Narration - 540 Cues)",
                    "isDraft": False
                }
            },
            media_body=MediaFileUpload(str(captions_path), mimetype="application/x-subrip")
        ).execute()
        print("[CAPTIONS] Successfully uploaded closed captions!")
    except Exception as e:
        print(f"[CAPTIONS ERROR] Could not upload captions: {e}")

def main():
    parser = argparse.ArgumentParser(description="Upload Master Supercut to YouTube with Full Metadata")
    parser.add_argument("--privacy", choices=["public", "private", "unlisted"], default="unlisted", help="Video privacy setting (default: unlisted)")
    parser.add_argument("--title", default=DEFAULT_TITLE, help="Custom title for the video")
    parser.add_argument("--video", default=str(DEFAULT_VIDEO_PATH), help="Path to master mp4")
    parser.add_argument("--thumbnail", default=str(DEFAULT_THUMBNAIL_PATH), help="Path to 16:9 thumbnail")
    parser.add_argument("--captions", default=str(DEFAULT_CAPTIONS_PATH), help="Path to .srt captions")
    parser.add_argument("--client-secrets", default=str(DEFAULT_CLIENT_SECRETS), help="Path to OAuth client_secret.json")
    parser.add_argument("--token", default=str(DEFAULT_TOKEN_PATH), help="Path to token.json")
    parser.add_argument("--category", default="27", help="YouTube Category ID (27 = Education)")
    args = parser.parse_args()

    print("===================================================================")
    print("  THE CURIOSITY KILLS THE CAT: YOUTUBE API SUPERCUT PUBLISHER")
    print("===================================================================")

    client_secrets = Path(args.client_secrets)
    token_file = Path(args.token)
    video_path = Path(args.video)
    thumbnail_path = Path(args.thumbnail)
    captions_path = Path(args.captions)

    youtube = get_authenticated_service(client_secrets, token_file)
    description = load_description_with_chapters()
    video_id = upload_video(youtube, video_path, args.title, description, DEFAULT_TAGS, args.privacy, args.category)

    if video_id:
        set_thumbnail(youtube, video_id, thumbnail_path)
        upload_captions(youtube, video_id, captions_path)
        print("\n===================================================================")
        print(f"  UPLOAD COMPLETE: https://www.youtube.com/watch?v={video_id}")
        print("===================================================================")

if __name__ == "__main__":
    main()
