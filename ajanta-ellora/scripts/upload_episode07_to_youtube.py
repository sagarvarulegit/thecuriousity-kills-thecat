#!/usr/bin/env python3
"""
YouTube Data API v3 Complete Release Pipeline for Episode 07 + Companion Shorts
Channel: thecuriousity-kills-thecat

Workflow:
  1. Resumable upload of Episode 07 Long-Form Master (1080p, 307 MB)
     - Exponential backoff retry loop (socket errors, DNS drops, HTTP 5xx)
  2. Thumbnail upload (16:9 custom thumbnail)
  3. Caption upload (English .srt + Hindi .srt)
  4. Fetch Episode 07 Watch URL
  5. Resumable upload of Short 01 (9:16 vertical 1080x1920)
     - 9:16 vertical thumbnail
     - Description with Episode 07 Watch URL
     - Conversion funnel top comment with Episode 07 Watch URL
  6. Resumable upload of Short 02 (9:16 vertical 1080x1920)
     - 9:16 vertical thumbnail
     - Description with Episode 07 Watch URL
     - Conversion funnel top comment with Episode 07 Watch URL
  7. Output release summary with YouTube Studio deep-links for "Related video" tagging.
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
EP07_DIR = WORKSPACE_ROOT / "ajanta-ellora" / "episode07"
VIDEOS_DIR = EP07_DIR / "final_videos"
THUMB_DIR = EP07_DIR / "thumbnail"

DEFAULT_VIDEO_PATH = VIDEOS_DIR / "episode_07_the_secret_canyon_of_waghur_master_1080p.mp4"
DEFAULT_THUMBNAIL_PATH = THUMB_DIR / "ep07_thumbnail_16x9_the_secret_canyon.jpg"
DEFAULT_CAPTIONS_PATH = EP07_DIR / "subtitles" / "episode_07_full.srt"
DEFAULT_HINDI_CAPTIONS_PATH = EP07_DIR / "subtitles_hindi" / "episode_07_hindi_full.srt"
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
0:32 - The Hidden Amphitheater of Waghur
1:16 - The Satavahana Inception & Top-Down Chisel Strikes
2:55 - Taming the Monsoon: Subterranean Hydraulic Defense
4:25 - The Sound of the Living Stone: Acoustic Archaeology
5:35 - The 400-Year Hibernation & The Mystery to Come

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
                raise FileNotFoundError(f"[ERROR] OAuth client secrets file not found: {client_secrets_file}")
            print(f"[AUTH] Starting OAuth 2.0 Web Authorization flow using {client_secrets_file}...")
            flow = InstalledAppFlow.from_client_secrets_file(str(client_secrets_file), SCOPES)
            creds = flow.run_local_server(port=0)

        with open(token_file, "w") as token:
            token.write(creds.to_json())
            print(f"[AUTH] Credentials saved to {token_file} for future uploads.")

    return build(API_SERVICE_NAME, API_VERSION, credentials=creds)


def upload_video_resumable(youtube, video_path: Path, title: str, description: str, tags: list, privacy_status: str, category_id: str = "27", chunk_mb: int = 16):
    """Resumable video upload with exponential backoff on network errors."""
    if not video_path.exists():
        raise FileNotFoundError(f"Video file not found at {video_path}")

    file_size_mb = os.path.getsize(video_path) / (1024 * 1024)
    print(f"\n[UPLOAD] Initiating upload: {video_path.name} ({file_size_mb:.2f} MB)")
    print(f"[UPLOAD] Title: {title}")
    print(f"[UPLOAD] Privacy: {privacy_status} | Category ID: {category_id}")

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

    chunksize = chunk_mb * 1024 * 1024
    media = MediaFileUpload(str(video_path), chunksize=chunksize, resumable=True, mimetype="video/mp4")

    request = youtube.videos().insert(
        part="snippet,status",
        body=body,
        media_body=media
    )

    response = None
    retry_count = 0
    max_retries = 20
    start_time = time.time()

    print("[UPLOAD] Transferring chunks...")
    while response is None:
        try:
            status, response = request.next_chunk()
            if status:
                progress = int(status.progress() * 100)
                uploaded_mb = (status.resumable_progress or 0) / (1024 * 1024)
                elapsed = time.time() - start_time
                print(f"  -> Uploaded: {progress}% ({uploaded_mb:.1f}/{file_size_mb:.1f} MB, {elapsed:.1f}s elapsed)", flush=True)
            retry_count = 0  # Reset retry counter on successful chunk
        except (HttpError, httplib2.HttpLib2Error, http.client.HTTPException, socket.error, Exception) as e:
            retry_count += 1
            if retry_count > max_retries:
                print(f"[FATAL] Max retries exceeded ({max_retries}). Aborting.")
                raise e
            wait_time = min(2 ** retry_count, 60)
            print(f"  [WARN] Network error ({e}). Retrying chunk in {wait_time}s (attempt {retry_count}/{max_retries})...", flush=True)
            time.sleep(wait_time)

    video_id = response.get("id")
    print(f"\n[SUCCESS] Upload complete! Video ID: {video_id}")
    print(f"[LINK] Watch URL: https://www.youtube.com/watch?v={video_id}")
    return video_id


def upload_thumbnail(youtube, video_id: str, thumbnail_path: Path):
    """Set custom thumbnail for the video."""
    if not thumbnail_path.exists():
        print(f"[WARN] Thumbnail not found at {thumbnail_path}. Skipping.")
        return False

    thumb_size_kb = os.path.getsize(thumbnail_path) / 1024
    print(f"[THUMBNAIL] Uploading thumbnail: {thumbnail_path.name} ({thumb_size_kb:.1f} KB)...")
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


def upload_captions(youtube, video_id: str, captions_path: Path, language: str = "en", name: str = "English (Full Narration)"):
    """Upload subtitles to YouTube."""
    if not captions_path.exists():
        print(f"[WARN] Captions file not found at {captions_path}. Skipping.")
        return False

    print(f"[CAPTIONS] Uploading {name} ({language}) subtitles from {captions_path.name}...")
    try:
        media = MediaFileUpload(str(captions_path), mimetype="text/plain")
        body = {
            "snippet": {
                "videoId": video_id,
                "language": language,
                "name": name,
                "isDraft": False
            }
        }
        youtube.captions().insert(
            part="snippet",
            body=body,
            media_body=media
        ).execute()
        print(f"[CAPTIONS] {name} subtitles attached successfully!")
        return True
    except Exception as e:
        print(f"[ERROR] Failed to upload {name} captions: {e}")
        return False


def post_funnel_comment(youtube, video_id: str, comment_text: str):
    """Post conversion comment linking to long-form video."""
    print(f"[COMMENT] Posting conversion comment to {video_id}...")
    try:
        resp = youtube.commentThreads().insert(
            part="snippet",
            body={
                "snippet": {
                    "videoId": video_id,
                    "topLevelComment": {
                        "snippet": {
                            "textOriginal": comment_text
                        }
                    }
                }
            }
        ).execute()
        comment_id = resp.get("id")
        print(f"[COMMENT] Comment posted successfully (ID: {comment_id})")
        return comment_id
    except Exception as e:
        print(f"[ERROR] Could not post comment: {e}")
        return None


def main():
    parser = argparse.ArgumentParser(description="Upload Episode 07 and Companion Shorts to YouTube.")
    parser.add_argument("--privacy", choices=["public", "unlisted", "private"], default="public", help="Video privacy (default: public)")
    parser.add_argument("--secrets", type=Path, default=DEFAULT_CLIENT_SECRETS, help="Path to client_secret.json")
    parser.add_argument("--token", type=Path, default=DEFAULT_TOKEN_PATH, help="Path to token.json")
    parser.add_argument("--skip-longform", action="store_true", help="Skip long-form video upload (if already uploaded)")
    parser.add_argument("--longform-id", type=str, default="", help="Existing long-form video ID (if skipping long-form)")
    args = parser.parse_args()

    print("=" * 70)
    print("  THE CURIOSITY KILLS THE CAT: EPISODE 07 FULL RELEASE PIPELINE")
    print("=" * 70)

    youtube = get_authenticated_service(args.secrets, args.token)

    # STEP 1: Long-Form Video Upload
    longform_id = args.longform_id
    if not args.skip_longform:
        longform_id = upload_video_resumable(
            youtube,
            DEFAULT_VIDEO_PATH,
            DEFAULT_TITLE,
            DEFAULT_DESCRIPTION,
            DEFAULT_TAGS,
            args.privacy,
            category_id="27",
            chunk_mb=16
        )
        upload_thumbnail(youtube, longform_id, DEFAULT_THUMBNAIL_PATH)
        upload_captions(youtube, longform_id, DEFAULT_CAPTIONS_PATH, language="en", name="English (Full Narration)")
        upload_captions(youtube, longform_id, DEFAULT_HINDI_CAPTIONS_PATH, language="hi", name="Hindi")
    else:
        print(f"[INFO] Skipping longform upload. Using existing ID: {longform_id}")

    if not longform_id:
        print("[FATAL] No long-form video ID available. Cannot proceed to Shorts.")
        sys.exit(1)

    longform_url = f"https://www.youtube.com/watch?v={longform_id}"
    print(f"\n>>> EPISODE 07 LIVE AT: {longform_url} <<<\n")

    # STEP 2: Companion Shorts Upload (With Long-Form URL Injected)
    uploaded_shorts = []
    for cfg in SHORTS_CONFIG:
        print("-" * 70)
        print(f"  UPLOADING COMPANION SHORT: {cfg['id'].upper()}")
        print("-" * 70)

        desc = cfg["desc_template"].format(longform_url=longform_url)
        short_id = upload_video_resumable(
            youtube,
            cfg["video_file"],
            cfg["title"],
            desc,
            cfg["tags"],
            args.privacy,
            category_id="27",
            chunk_mb=8
        )
        upload_thumbnail(youtube, short_id, cfg["thumb_file"])

        comment_text = cfg["comment_template"].format(longform_url=longform_url)
        post_funnel_comment(youtube, short_id, comment_text)

        uploaded_shorts.append({
            "id": short_id,
            "title": cfg["title"],
            "url": f"https://www.youtube.com/shorts/{short_id}",
            "studio_url": f"https://studio.youtube.com/video/{short_id}/edit"
        })

    # FINAL REPORT
    print("\n" + "=" * 70)
    print("  EPISODE 07 & COMPANION SHORTS RELEASE COMPLETE")
    print("=" * 70)
    print(f"  * MASTER DOCUMENTARY:")
    print(f"    Title:     {DEFAULT_TITLE}")
    print(f"    Watch URL: {longform_url}")
    print(f"    Privacy:   {args.privacy.upper()}")
    print()
    print("  * COMPANION SHORTS (9:16 VERTICAL):")
    for s in uploaded_shorts:
        print(f"    - Title:      {s['title']}")
        print(f"      Short URL:  {s['url']}")
        print(f"      Studio Edit:{s['studio_url']}")
        print(f"      Action:     Select 'Related video' -> {longform_id}")
    print("=" * 70)


if __name__ == "__main__":
    main()
