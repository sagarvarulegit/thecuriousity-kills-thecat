#!/usr/bin/env python3
"""
upload_episode08_to_youtube.py — YouTube Data API v3 Complete Release Pipeline for Episode 08 + Companion Shorts
Channel: thecuriousity-kills-thecat

Workflow:
  1. Resumable upload of Episode 08 Long-Form Master (1080p)
     - Exponential backoff retry loop (socket errors, DNS drops, HTTP 5xx)
  2. Thumbnail upload (16:9 custom thumbnail)
  3. Caption upload (English .srt)
  4. Fetch Episode 08 Watch URL
  5. Resumable upload of Short 01 (9:16 vertical 1080x1920)
     - 9:16 vertical thumbnail
     - Description with Episode 08 Watch URL
     - Conversion funnel top comment with Episode 08 Watch URL
  6. Resumable upload of Short 02 (9:16 vertical 1080x1920)
     - 9:16 vertical thumbnail
     - Description with Episode 08 Watch URL
     - Conversion funnel top comment with Episode 08 Watch URL
  7. Output release summary with YouTube Studio deep-links for "Related video" tagging and 1-click comment pinning.
"""

import os
import sys
import time
import socket
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

# Scopes required for upload, thumbnail, captions, and comments
SCOPES = [
    "https://www.googleapis.com/auth/youtube.upload",
    "https://www.googleapis.com/auth/youtube.force-ssl",
    "https://www.googleapis.com/auth/youtube"
]

API_SERVICE_NAME = "youtube"
API_VERSION = "v3"

WORKSPACE_ROOT = Path(__file__).resolve().parent.parent.parent
EP08_DIR = WORKSPACE_ROOT / "ajanta-ellora" / "episode08"
VIDEOS_DIR = EP08_DIR / "final_videos"
THUMB_DIR = EP08_DIR / "thumbnail"

DEFAULT_VIDEO_PATH = VIDEOS_DIR / "episode_08_master_1080p.mp4"
DEFAULT_THUMBNAIL_PATH = THUMB_DIR / "ep08_thumbnail_16x9_the_secret_chemistry.jpg"
DEFAULT_CAPTIONS_PATH = EP08_DIR / "subtitles" / "episode_08_full.srt"
DEFAULT_TOKEN_PATH = WORKSPACE_ROOT / "token.json"
DEFAULT_CLIENT_SECRETS = WORKSPACE_ROOT / "client_secret.json"

DEFAULT_TITLE = "The 1,500-Year-Old Paint Chemistry Modern Science Still Can't Replicate | Ajanta Caves"

DEFAULT_DESCRIPTION = """How did ancient Indian painters create the world's most expressive subterranean frescoes 40 meters inside pitch-black mountain caves—without leaving a single drop of torch soot?

In the late 5th century CE, Emperor Harishena of the Vakataka dynasty reawakened the dormant horseshoe canyon of Ajanta in an unprecedented explosion of royal patronage. To paint directly on damp, non-porous volcanic basalt, master guilds engineered a revolutionary 3-layer bio-composite plaster made of fermented red clay, cow dung cellulose, rice husks, and agate-burnished slaked lime. Across the ceilings, they applied pure ultramarine blue made of crushed lapis lazuli—mined 2,500 kilometers away in the snowy mountains of Badakhshan, Afghanistan, and worth more than solid gold.

To see in total darkness, ancient engineers bounced collimated natural sunlight off massive polished cast-bronze mirrors through the cave portals, diffusing the beams through wet white linen sheets to paint with captured sunlight. Then—in 477 CE—the empire suddenly collapsed, freezing the masterpieces in time.

TIMESTAMPS:
0:00 - The Golden Reawakening (Harishena's Renaissance)
1:32 - The Basalt Problem & The 3-Layer Mud Chemistry Secret
3:58 - The Silk Road Blue (Badakhshan Lapis Lazuli Alchemy)
5:41 - The Sootless Cave: Subterranean Optical Engineering
7:41 - Masterpieces of Humanity: Padmapani & The Looming Shadow

🔔 Subscribe to @thecuriousity-kills-thecat for deep-dive historical engineering documentaries.

#AjantaCaves #AncientEngineering #AncientPaintings #LapisLazuli #HistoryDocumentary #AncientIndia #SilkRoad #Padmapani"""

DEFAULT_TAGS = [
    "ajanta caves",
    "ajanta frescoes",
    "ancient paint chemistry",
    "lapis lazuli",
    "ancient engineering",
    "padmapani",
    "vakataka dynasty",
    "harishena",
    "silk road trade",
    "ancient pigments",
    "subterranean architecture",
    "ancient india",
    "cave paintings",
    "ancient technology",
    "history documentary"
]

DEFAULT_PINNED_COMMENT = """🏛️ If ancient painters in 460 CE could illuminate 40-meter-deep subterranean caves using only bronze mirrors and formulate mold-resistant bio-plasters that survived 1,500 years of monsoons, what other lost technologies were buried with ancient empires?

Let us know your theories below! 👇

🔔 Subscribe to @thecuriousity-kills-thecat for deep-dive ancient engineering investigations."""

SHORT_01_CONFIG = {
    "title": "The Secret Recipe Behind 1,500-Year-Old Cave Paintings #shorts",
    "video_path": VIDEOS_DIR / "short_01_the_mud_chemistry_secret_1080x1920.mp4",
    "thumbnail_path": THUMB_DIR / "short_01_thumbnail_9x16.jpg",
    "tags": [
        "ajanta caves", "ancient chemistry", "cave paintings", "ancient india", 
        "ancient engineering", "history shorts", "archaeology mysteries"
    ],
    "comment": "How did ancient organic mud survive 1,500 years of damp monsoons? Watch our full engineering documentary on Ajanta's paint chemistry linked above! 🏛️"
}

SHORT_02_CONFIG = {
    "title": "How Ancient Artists Painted in Total Darkness Without Fire #shorts",
    "video_path": VIDEOS_DIR / "short_02_the_bronze_mirror_secret_1080x1920.mp4",
    "thumbnail_path": THUMB_DIR / "short_02_thumbnail_9x16.jpg",
    "tags": [
        "ajanta caves", "ancient optics", "bronze mirror", "ancient engineering", 
        "ancient technology", "history shorts", "padmapani"
    ],
    "comment": "Discover how ancient engineers collimated natural sunlight deep into subterranean caves. Watch our full documentary linked above! 🏛️"
}

def get_authenticated_service(token_path: Path, client_secrets_path: Path):
    creds = None
    if token_path.exists():
        try:
            creds = Credentials.from_authorized_user_file(str(token_path), SCOPES)
        except Exception as e:
            print(f"[AUTH] Could not load token.json: {e}")

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            print("[AUTH] Refreshing expired OAuth credentials...")
            creds.refresh(Request())
            with open(token_path, "w", encoding="utf-8") as token_file:
                token_file.write(creds.to_json())
        else:
            if not client_secrets_path.exists():
                raise FileNotFoundError(f"Missing OAuth client_secret.json at: {client_secrets_path}")
            print("[AUTH] Launching local browser OAuth flow...")
            flow = InstalledAppFlow.from_client_secrets_file(str(client_secrets_path), SCOPES)
            creds = flow.run_local_server(port=0)
            with open(token_path, "w", encoding="utf-8") as token_file:
                token_file.write(creds.to_json())

    return build(API_SERVICE_NAME, API_VERSION, credentials=creds)

def upload_video_resumable(youtube, file_path: Path, title: str, description: str, tags: list, category_id: str = "27", privacy_status: str = "public", is_short: bool = False) -> str:
    print(f"\n[*] Initializing upload for: {file_path.name}")
    print(f"    Size: {file_path.stat().st_size / (1024*1024):.2f} MB | Privacy: {privacy_status}")

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

    chunksize = 8 * 1024 * 1024 if is_short else 16 * 1024 * 1024
    media = MediaFileUpload(str(file_path), mimetype="video/mp4", chunksize=chunksize, resumable=True)

    request = youtube.videos().insert(part="snippet,status", body=body, media_body=media)

    response = None
    retry_count = 0
    max_retries = 20

    while response is None:
        try:
            status, response = request.next_chunk()
            if status:
                print(f"    Upload progress: {int(status.progress() * 100)}% ({status.resumable_progress / (1024*1024):.1f} MB uploaded)")
            retry_count = 0
        except (HttpError, socket.error, socket.gaierror, http.client.HTTPException, httplib2.HttpLib2Error) as e:
            retry_count += 1
            if retry_count > max_retries:
                raise RuntimeError(f"Exceeded max upload retries ({max_retries}): {e}")
            sleep_sec = min(2 ** retry_count, 60)
            print(f"    [WARN] Transient error ({e}). Backing off {sleep_sec}s (retry {retry_count}/{max_retries})...")
            time.sleep(sleep_sec)

    video_id = response.get("id")
    print(f"[OK] Video successfully uploaded! ID: {video_id}")
    return video_id

def set_custom_thumbnail(youtube, video_id: str, thumbnail_path: Path):
    if not thumbnail_path.exists():
        print(f"[WARN] Thumbnail not found: {thumbnail_path}")
        return
    print(f"[*] Setting custom thumbnail: {thumbnail_path.name} for video {video_id}...")
    media = MediaFileUpload(str(thumbnail_path), mimetype="image/jpeg", resumable=False)
    try:
        youtube.thumbnails().set(videoId=video_id, media_body=media).execute()
        print(f"[OK] Custom thumbnail uploaded successfully.")
    except Exception as e:
        print(f"[WARN] Could not set custom thumbnail: {e}")

def upload_captions(youtube, video_id: str, srt_path: Path, language: str = "en", name: str = "English"):
    if not srt_path.exists():
        print(f"[WARN] Caption file not found: {srt_path}")
        return
    print(f"[*] Uploading {name} subtitles: {srt_path.name}...")
    media = MediaFileUpload(str(srt_path), mimetype="text/plain", resumable=False)
    body = {
        "snippet": {
            "videoId": video_id,
            "language": language,
            "name": name,
            "isDraft": False
        }
    }
    try:
        youtube.captions().insert(part="snippet", body=body, media_body=media).execute()
        print(f"[OK] Subtitles uploaded successfully.")
    except Exception as e:
        print(f"[WARN] Could not upload captions: {e}")

def post_comment(youtube, video_id: str, comment_text: str) -> str:
    print(f"[*] Posting comment on video {video_id}...")
    body = {
        "snippet": {
            "videoId": video_id,
            "topLevelComment": {
                "snippet": {
                    "textOriginal": comment_text
                }
            }
        }
    }
    try:
        resp = youtube.commentThreads().insert(part="snippet", body=body).execute()
        comment_id = resp["snippet"]["topLevelComment"]["id"]
        print(f"[OK] Comment posted! ID: {comment_id}")
        return comment_id
    except Exception as e:
        print(f"[WARN] Could not post comment: {e}")
        return ""

def main():
    parser = argparse.ArgumentParser(description="Upload Episode 08 and Companion Shorts to YouTube")
    parser.add_argument("--dry-run", action="store_true", help="Perform checks without uploading")
    parser.add_argument("--privacy", default="public", choices=["public", "unlisted", "private"], help="Privacy status")
    args = parser.parse_args()

    print("=" * 65)
    print("  EPISODE 08 COMPLETE YOUTUBE RELEASE PIPELINE")
    print("=" * 65)

    if args.dry_run:
        print("[DRY-RUN] Validating asset existence...")
        print(f"Master Video: {DEFAULT_VIDEO_PATH.exists()}")
        print(f"Master Thumbnail: {DEFAULT_THUMBNAIL_PATH.exists()}")
        print(f"Master Captions: {DEFAULT_CAPTIONS_PATH.exists()}")
        print(f"Short 01 Video: {SHORT_01_CONFIG['video_path'].exists()}")
        print(f"Short 02 Video: {SHORT_02_CONFIG['video_path'].exists()}")
        return

    youtube = get_authenticated_service(DEFAULT_TOKEN_PATH, DEFAULT_CLIENT_SECRETS)

    # 1. Upload Long-form Master
    master_id = upload_video_resumable(
        youtube=youtube,
        file_path=DEFAULT_VIDEO_PATH,
        title=DEFAULT_TITLE,
        description=DEFAULT_DESCRIPTION,
        tags=DEFAULT_TAGS,
        privacy_status=args.privacy,
        is_short=False
    )
    master_url = f"https://www.youtube.com/watch?v={master_id}"
    set_custom_thumbnail(youtube, master_id, DEFAULT_THUMBNAIL_PATH)
    upload_captions(youtube, master_id, DEFAULT_CAPTIONS_PATH, language="en", name="English")
    master_comment_id = post_comment(youtube, master_id, DEFAULT_PINNED_COMMENT)

    # 2. Upload Short 01
    s1_desc = f"{SHORT_01_CONFIG['title']}\n\nWatch the full documentary deep-dive: {master_url}\n\n#AjantaCaves #AncientEngineering #Shorts"
    s1_id = upload_video_resumable(
        youtube=youtube,
        file_path=SHORT_01_CONFIG["video_path"],
        title=SHORT_01_CONFIG["title"],
        description=s1_desc,
        tags=SHORT_01_CONFIG["tags"],
        privacy_status=args.privacy,
        is_short=True
    )
    set_custom_thumbnail(youtube, s1_id, SHORT_01_CONFIG["thumbnail_path"])
    s1_comment_text = f"{SHORT_01_CONFIG['comment']}\n\n👉 Full Documentary: {master_url}"
    s1_comment_id = post_comment(youtube, s1_id, s1_comment_text)

    # 3. Upload Short 02
    s2_desc = f"{SHORT_02_CONFIG['title']}\n\nWatch the full documentary deep-dive: {master_url}\n\n#AjantaCaves #AncientEngineering #Shorts"
    s2_id = upload_video_resumable(
        youtube=youtube,
        file_path=SHORT_02_CONFIG["video_path"],
        title=SHORT_02_CONFIG["title"],
        description=s2_desc,
        tags=SHORT_02_CONFIG["tags"],
        privacy_status=args.privacy,
        is_short=True
    )
    set_custom_thumbnail(youtube, s2_id, SHORT_02_CONFIG["thumbnail_path"])
    s2_comment_text = f"{SHORT_02_CONFIG['comment']}\n\n👉 Full Documentary: {master_url}"
    s2_comment_id = post_comment(youtube, s2_id, s2_comment_text)

    # Release Summary
    print("\n" + "=" * 65)
    print("  EPISODE 08 RELEASE SUCCESSFUL!")
    print("=" * 65)
    print(f"Master Documentary: {master_url}")
    print(f"  Studio Edit URL: https://studio.youtube.com/video/{master_id}/edit")
    if master_comment_id:
        print(f"  Pin Comment Link: https://www.youtube.com/watch?v={master_id}&lc={master_comment_id}")
    print(f"\nShort 01: https://www.youtube.com/shorts/{s1_id}")
    print(f"  Studio Edit URL: https://studio.youtube.com/video/{s1_id}/edit")
    if s1_comment_id:
        print(f"  Pin Comment Link: https://www.youtube.com/watch?v={s1_id}&lc={s1_comment_id}")
    print(f"\nShort 02: https://www.youtube.com/shorts/{s2_id}")
    print(f"  Studio Edit URL: https://studio.youtube.com/video/{s2_id}/edit")
    if s2_comment_id:
        print(f"  Pin Comment Link: https://www.youtube.com/watch?v={s2_id}&lc={s2_comment_id}")
    print("=" * 65)

if __name__ == "__main__":
    main()
