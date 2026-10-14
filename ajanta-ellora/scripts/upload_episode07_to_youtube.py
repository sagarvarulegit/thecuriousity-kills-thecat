#!/usr/bin/env python3
"""
YouTube Data API v3 Video & Metadata Uploader for Episode 07
Channel: thecuriousity-kills-thecat
Automates:
  1. Resumable video upload (Full HD master 1080p)
  2. Thumbnail upload (16:9 custom thumbnail)
  3. Caption upload (English .srt subtitles)
  4. Complete SEO metadata (Title, Description with timestamps, Tags, Category)
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

# Default File Paths for Episode 07
WORKSPACE_ROOT = Path(__file__).resolve().parent.parent.parent
DEFAULT_VIDEO_PATH = WORKSPACE_ROOT / "ajanta-ellora" / "episode07" / "final_videos" / "episode_07_the_secret_canyon_of_waghur_master_1080p.mp4"
DEFAULT_THUMBNAIL_PATH = WORKSPACE_ROOT / "ajanta-ellora" / "episode07" / "thumbnail" / "ep07_thumbnail_16x9_the_secret_canyon.jpg"
DEFAULT_CAPTIONS_PATH = WORKSPACE_ROOT / "ajanta-ellora" / "episode07" / "subtitles" / "episode_07_narration.srt"
DEFAULT_TOKEN_PATH = WORKSPACE_ROOT / "token.json"
DEFAULT_CLIENT_SECRETS = WORKSPACE_ROOT / "client_secret.json"

# Master Publish Kit Metadata for Episode 07
DEFAULT_TITLE = "The 1,300-Year Mystery Hidden in a Volcanic Canyon | Ajanta Caves"

DEFAULT_DESCRIPTION = """Before a single chisel struck the mountain at Kailasa, ancient engineers had already mastered the art of subterranean excavation 100 kilometers away—in a jagged, crescent canyon carved by the Waghur River.

Hidden behind sheer 75-meter volcanic basalt cliffs and dense teak jungle, the 30 rock-cut sanctuaries of Ajanta represent over 700 years of geotechnical, hydraulic, and acoustic mastery. In this episode, we journey back to the 2nd century BCE to uncover how early Satavahana monks hollowed out monumental vaulted chaityas from the roofline down without scaffolding, engineered surface bedrock drainage channels to withstand torrential monsoons, and tuned living rock chambers into colossal acoustic resonators.

Then—in the 1st century CE—work abruptly stopped. For 400 uninterrupted years, Ajanta lay completely dormant, frozen in time, waiting for an emperor who would awaken it in an explosion of gold and Afghan blue gems.

🔔 Subscribe to @thecuriousity-kills-thecat for deep-dive historical engineering documentaries.

TIMESTAMPS:
0:00 - The Monolith in the Abyss (The Pivot from Kailasa)
0:48 - The Hidden Amphitheater of Waghur
1:38 - The Satavahana Inception & Top-Down Chisel Strikes
2:30 - Taming the Monsoon: Subterranean Hydraulic Defense
3:55 - The Sound of the Living Stone: Acoustic Archaeology
5:21 - The 400-Year Hibernation & The Mystery to Come

#AjantaCaves #AncientEngineering #KailasaTemple #IndianArchaeology #HistoryDocumentary #AncientIndia #Architecture"""

DEFAULT_TAGS = [
    "ajanta caves",
    "ajanta ellora documentary",
    "kailasa temple",
    "ancient indian engineering",
    "rock cut architecture",
    "satavahana dynasty",
    "deccan traps basalt",
    "ancient hydrology",
    "acoustic archaeology",
    "ancient technology",
    "buddhist caves",
    "ancient mysteries",
    "india documentary",
    "monolithic temple",
    "ancient quarrying"
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

        # Save credentials for future executions
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
            "selfDeclaredMadeForKids": False,
            "embeddable": True,
            "license": "youtube"
        }
    }

    # 8MB chunk size for reliable resumable upload
    media = MediaFileUpload(str(video_path), chunksize=8 * 1024 * 1024, resumable=True, mimetype="video/mp4")

    request = youtube.videos().insert(
        part="snippet,status",
        body=body,
        media_body=media
    )

    response = None
    start_time = time.time()

    print("[UPLOAD] Upload in progress...")
    while response is None:
        status, response = request.next_chunk()
        if status:
            progress = int(status.progress() * 100)
            elapsed = time.time() - start_time
            print(f"  -> Uploaded: {progress}% (Elapsed: {elapsed:.1f}s)", flush=True)

    video_id = response.get("id")
    print(f"\n[SUCCESS] Video uploaded successfully! Video ID: {video_id}")
    print(f"[LINK] Watch URL: https://www.youtube.com/watch?v={video_id}")
    return video_id


def upload_thumbnail(youtube, video_id: str, thumbnail_path: Path):
    """Set custom thumbnail for the uploaded video."""
    if not thumbnail_path.exists():
        print(f"[WARN] Thumbnail not found at {thumbnail_path}. Skipping.")
        return False

    thumb_size_kb = os.path.getsize(thumbnail_path) / 1024
    print(f"\n[THUMBNAIL] Uploading custom thumbnail: {thumbnail_path.name} ({thumb_size_kb:.1f} KB)...")
    try:
        media = MediaFileUpload(str(thumbnail_path), mimetype="image/jpeg")
        youtube.thumbnails().set(
            videoId=video_id,
            media_body=media
        ).execute()
        print("[THUMBNAIL] Custom thumbnail applied successfully!")
        return True
    except Exception as e:
        print(f"[ERROR] Failed to set thumbnail: {e}")
        return False


def upload_captions(youtube, video_id: str, captions_path: Path):
    """Upload English subtitles to YouTube."""
    if not captions_path.exists():
        print(f"[WARN] Captions file not found at {captions_path}. Skipping.")
        return False

    print(f"\n[CAPTIONS] Uploading .srt subtitles from {captions_path.name}...")
    try:
        media = MediaFileUpload(str(captions_path), mimetype="text/plain")
        body = {
            "snippet": {
                "videoId": video_id,
                "language": "en",
                "name": "English (Full Narration)",
                "isDraft": False
            }
        }
        youtube.captions().insert(
            part="snippet",
            body=body,
            media_body=media
        ).execute()
        print("[CAPTIONS] Subtitles attached and published successfully!")
        return True
    except Exception as e:
        print(f"[ERROR] Failed to upload captions: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(description="Upload Episode 07 to YouTube via Data API v3.")
    parser.add_argument("--video", type=Path, default=DEFAULT_VIDEO_PATH, help="Path to master .mp4")
    parser.add_argument("--thumbnail", type=Path, default=DEFAULT_THUMBNAIL_PATH, help="Path to 16:9 thumbnail")
    parser.add_argument("--captions", type=Path, default=DEFAULT_CAPTIONS_PATH, help="Path to .srt captions")
    parser.add_argument("--secrets", type=Path, default=DEFAULT_CLIENT_SECRETS, help="Path to client_secret.json")
    parser.add_argument("--token", type=Path, default=DEFAULT_TOKEN_PATH, help="Path to token.json")
    parser.add_argument("--title", type=str, default=DEFAULT_TITLE, help="Video title")
    parser.add_argument("--privacy", type=str, choices=["public", "unlisted", "private"], default="unlisted", help="Privacy status (default: unlisted for safety)")
    parser.add_argument("--category", type=str, default="27", help="YouTube Category ID (27 = Education)")

    args = parser.parse_args()

    print("=" * 70)
    print("  YOUTUBE PUBLISHER: EPISODE 07 — THE SECRET CANYON OF WAGHUR")
    print("=" * 70)

    try:
        youtube = get_authenticated_service(args.secrets, args.token)
        video_id = upload_video(
            youtube,
            args.video,
            args.title,
            DEFAULT_DESCRIPTION,
            DEFAULT_TAGS,
            args.privacy,
            args.category
        )

        upload_thumbnail(youtube, video_id, args.thumbnail)
        upload_captions(youtube, video_id, args.captions)

        print("\n" + "=" * 70)
        print("  PUBLICATION COMPLETED SUCCESSFULLY")
        print(f"  Video URL: https://www.youtube.com/watch?v={video_id}")
        print(f"  Privacy:   {args.privacy.upper()}")
        print("=" * 70)

    except Exception as e:
        print(f"\n[FATAL ERROR] {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
