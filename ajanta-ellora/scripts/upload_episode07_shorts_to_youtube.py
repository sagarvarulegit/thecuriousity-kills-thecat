#!/usr/bin/env python3
"""
YouTube Data API v3 Uploader for Episode 07 Companion Shorts
Channel: thecuriousity-kills-thecat
Automates:
  1. Uploading Short 01 & Short 02 (9:16 vertical 1080x1920)
  2. Setting custom 9:16 mobile thumbnails
  3. Inserting the Episode 07 Long-Form Watch URL into descriptions
  4. Posting top-level conversion comments linking to Episode 07
"""

import os
import sys
import time
import argparse
from pathlib import Path

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

SCOPES = [
    "https://www.googleapis.com/auth/youtube.upload",
    "https://www.googleapis.com/auth/youtube.force-ssl",
    "https://www.googleapis.com/auth/youtube"
]

WORKSPACE_ROOT = Path(__file__).resolve().parent.parent.parent
EP07_DIR = WORKSPACE_ROOT / "ajanta-ellora" / "episode07"
VIDEOS_DIR = EP07_DIR / "final_videos"
THUMB_DIR = EP07_DIR / "thumbnail"
DEFAULT_TOKEN_PATH = WORKSPACE_ROOT / "token.json"
DEFAULT_CLIENT_SECRETS = WORKSPACE_ROOT / "client_secret.json"

SHORTS_CONFIG = [
    {
        "id": "short_01",
        "video_file": VIDEOS_DIR / "short_01_the_horseshoe_canyon_hidden_from_the_world_1080x1920.mp4",
        "thumb_file": THUMB_DIR / "short_01_thumbnail_9x16.jpg",
        "title": "They Carved 30 Temples Into Living Rock—Then Vanished #shorts",
        "desc_template": (
            "Over 2,000 years ago, ancient builders carved 30 monolithic temples directly into a 75-meter volcanic canyon wall—without scaffolding or mortar. Then, they abruptly abandoned the site to the jungle for 1,300 years.\n\n"
            "👉 WATCH THE FULL DOCUMENTARY INVESTIGATION:\n"
            "➡️ {longform_url}\n\n"
            "🔔 Subscribe to @thecuriousity-kills-thecat for deep-dive ancient engineering investigations.\n\n"
            "#Shorts #AjantaCaves #AncientEngineering #Archaeology #HistoryMysteries #AncientIndia #LostCivilization #Megaliths"
        ),
        "tags": [
            "ajanta caves", "shorts", "ancient engineering", "kailasa temple",
            "rock cut caves", "ancient india", "buddhist temples", "viral history",
            "ancient architecture", "megaliths", "lost civilization",
            "archaeology documentary", "mountain carving", "ancient builders"
        ],
        "comment_template": (
            "🏛️ How did ancient builders hollow out a 75-meter volcanic canyon wall with zero scaffolding and zero mistakes?\n\n"
            "The engineering breakthrough that led to Kailasa Temple started right here.\n\n"
            "👉 WATCH THE FULL INVESTIGATION HERE:\n"
            "➡️ {longform_url}"
        )
    },
    {
        "id": "short_02",
        "video_file": VIDEOS_DIR / "short_02_how_ancient_monks_engineered_water_1080x1920.mp4",
        "thumb_file": THUMB_DIR / "short_02_thumbnail_9x16.jpg",
        "title": "Monsoon Floods Tried to Drown This Monastery (They Failed) #shorts",
        "desc_template": (
            "When brutal monsoon rains threatened to wash 30 ancient temples down a 75-meter volcanic canyon, ancient monks didn't run. They carved an ingenious subterranean hydraulic system directly into solid bedrock.\n\n"
            "👉 WATCH THE FULL DOCUMENTARY INVESTIGATION:\n"
            "➡️ {longform_url}\n\n"
            "🔔 Subscribe to @thecuriousity-kills-thecat for deep-dive ancient engineering investigations.\n\n"
            "#Shorts #AncientEngineering #AjantaCaves #WaterFiltration #AncientCivilization #Archaeology #HydraulicEngineering #Monsoon"
        ),
        "tags": [
            "ajanta caves", "ancient engineering", "monsoon engineering",
            "hydraulic engineering", "ancient india", "ancient technology",
            "rock cut architecture", "history shorts", "ancient cisterns",
            "water filtration", "archaeology documentary", "monolithic engineering"
        ],
        "comment_template": (
            "🌊 How did ancient monks protect 30 temples from drowning under millions of gallons of raging monsoon floodwaters?\n\n"
            "Their 2,000-year-old rock-carved hydraulic filtration system still works today.\n\n"
            "👉 WATCH THE FULL INVESTIGATION HERE:\n"
            "➡️ {longform_url}"
        )
    }
]


def get_authenticated_service(client_secrets_file: Path, token_file: Path):
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
                raise FileNotFoundError(f"[ERROR] OAuth client secrets file not found: {client_secrets_file}")
            print(f"[AUTH] Starting OAuth 2.0 Web Authorization flow using {client_secrets_file}...")
            flow = InstalledAppFlow.from_client_secrets_file(str(client_secrets_file), SCOPES)
            creds = flow.run_local_server(port=0)

        with open(token_file, "w") as token:
            token.write(creds.to_json())
            print(f"[AUTH] Credentials saved to {token_file}.")

    return build("youtube", "v3", credentials=creds)


def upload_short(youtube, config: dict, longform_url: str, privacy_status: str, category_id: str = "27"):
    video_path = config["video_file"]
    if not video_path.exists():
        raise FileNotFoundError(f"Short video not found at {video_path}")

    file_size_mb = os.path.getsize(video_path) / (1024 * 1024)
    title = config["title"]
    description = config["desc_template"].format(longform_url=longform_url)
    tags = config["tags"]

    print(f"\n[UPLOAD SHORTS] Initiating upload: {video_path.name} ({file_size_mb:.2f} MB)")
    print(f"[UPLOAD SHORTS] Title: {title}")
    print(f"[UPLOAD SHORTS] Privacy: {privacy_status}")

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

    media = MediaFileUpload(str(video_path), chunksize=4 * 1024 * 1024, resumable=True, mimetype="video/mp4")
    request = youtube.videos().insert(
        part="snippet,status",
        body=body,
        media_body=media
    )

    response = None
    start_time = time.time()
    print("[UPLOAD] Transferring chunks...")
    while response is None:
        status, response = request.next_chunk()
        if status:
            progress = int(status.progress() * 100)
            elapsed = time.time() - start_time
            print(f"  -> Uploaded: {progress}% (Elapsed: {elapsed:.1f}s)", flush=True)

    short_id = response.get("id")
    print(f"[SUCCESS] Short uploaded! Video ID: {short_id}")
    print(f"[LINK] Short URL: https://www.youtube.com/shorts/{short_id}")

    # Set Custom 9:16 Thumbnail
    thumb_path = config["thumb_file"]
    if thumb_path.exists():
        try:
            print(f"[THUMBNAIL] Applying 9:16 vertical thumbnail: {thumb_path.name}...")
            youtube.thumbnails().set(
                videoId=short_id,
                media_body=MediaFileUpload(str(thumb_path), mimetype="image/jpeg")
            ).execute()
            print("[THUMBNAIL] Successfully applied custom thumbnail!")
        except Exception as e:
            print(f"[THUMBNAIL ERROR] Could not set thumbnail: {e}")

    # Post Pinned Funnel Comment
    comment_text = config["comment_template"].format(longform_url=longform_url)
    try:
        print("[COMMENT] Posting conversion funnel comment...")
        comm_resp = youtube.commentThreads().insert(
            part="snippet",
            body={
                "snippet": {
                    "videoId": short_id,
                    "topLevelComment": {
                        "snippet": {
                            "textOriginal": comment_text
                        }
                    }
                }
            }
        ).execute()
        comment_id = comm_resp.get("id")
        print(f"[COMMENT] Posted comment ID: {comment_id}")
    except Exception as e:
        print(f"[COMMENT ERROR] Could not post funnel comment: {e}")

    return short_id


def main():
    parser = argparse.ArgumentParser(description="Upload Episode 07 Companion Shorts to YouTube.")
    parser.add_argument("--longform-url", required=True, help="Full watch URL of Episode 07 long-form video")
    parser.add_argument("--privacy", choices=["public", "unlisted", "private"], default="public", help="Shorts privacy (default: public)")
    parser.add_argument("--secrets", type=Path, default=DEFAULT_CLIENT_SECRETS, help="Path to client_secret.json")
    parser.add_argument("--token", type=Path, default=DEFAULT_TOKEN_PATH, help="Path to token.json")
    args = parser.parse_args()

    print("=" * 70)
    print("  YOUTUBE PUBLISHER: EPISODE 07 COMPANION SHORTS")
    print(f"  Target Long-Form Link: {args.longform_url}")
    print("=" * 70)

    youtube = get_authenticated_service(args.secrets, args.token)

    uploaded_shorts = []
    for cfg in SHORTS_CONFIG:
        short_id = upload_short(youtube, cfg, args.longform_url, args.privacy)
        uploaded_shorts.append({"id": short_id, "title": cfg["title"]})

    print("\n" + "=" * 70)
    print("  ALL COMPANION SHORTS UPLOADED SUCCESSFULLY!")
    print("=" * 70)
    for s in uploaded_shorts:
        print(f"  * {s['title']}")
        print(f"    Shorts URL: https://www.youtube.com/shorts/{s['id']}")
        print(f"    Studio Edit URL: https://studio.youtube.com/video/{s['id']}/edit (Select 'Related video' -> Ep 07)")
    print("=" * 70)


if __name__ == "__main__":
    main()
