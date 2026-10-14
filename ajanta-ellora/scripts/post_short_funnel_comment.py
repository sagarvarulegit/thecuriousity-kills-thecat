#!/usr/bin/env python3
"""
Post Conversion Funnel Comment on Viral Short cV_YoIUZM70
Channel: The Curiosity Kills The Cat
Directs viewers to the full Kailasa documentary (vqvxP-I5hCg)
"""

import sys
from pathlib import Path
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request

WORKSPACE_ROOT = Path(__file__).resolve().parent.parent.parent
TOKEN_FILE = WORKSPACE_ROOT / "token.json"
SCOPES = [
    "https://www.googleapis.com/auth/youtube.upload",
    "https://www.googleapis.com/auth/youtube.force-ssl",
    "https://www.googleapis.com/auth/youtube"
]

VIDEO_ID = "cV_YoIUZM70"
FULL_DOC_ID = "vqvxP-I5hCg"

COMMENT_TEXT = (
    "🏛️ How did 1,000 men with heavy iron chisels fail to break Kailasa Temple over 3 entire years?\n\n"
    "The secret wasn't magic—it was the impossible top-down structural geometry and zero-tolerance monolithic basalt carving.\n\n"
    f"👉 WATCH THE FULL 10-MINUTE INVESTIGATION HERE:\n"
    f"➡️ https://www.youtube.com/watch?v={FULL_DOC_ID}\n\n"
    "(What the survey teams uncovered behind the subterranean false wall broke every known law of ancient engineering!)"
)

def get_authenticated_service():
    if not TOKEN_FILE.exists():
        raise FileNotFoundError(f"Token file not found at {TOKEN_FILE}")
    creds = Credentials.from_authorized_user_file(str(TOKEN_FILE), SCOPES)
    if not creds.valid:
        if creds.expired and creds.refresh_token:
            print("[AUTH] Refreshing expired credentials...")
            creds.refresh(Request())
            with open(TOKEN_FILE, "w") as f:
                f.write(creds.to_json())
    return build("youtube", "v3", credentials=creds)

def main():
    print(f"[COMMENT] Connecting to YouTube API...")
    youtube = get_authenticated_service()
    
    print(f"[COMMENT] Posting top-level comment to video {VIDEO_ID}...")
    try:
        response = youtube.commentThreads().insert(
            part="snippet",
            body={
                "snippet": {
                    "videoId": VIDEO_ID,
                    "topLevelComment": {
                        "snippet": {
                            "textOriginal": COMMENT_TEXT
                        }
                    }
                }
            }
        ).execute()
        comment_id = response.get("id")
        print(f"[SUCCESS] Comment posted successfully! Comment ID: {comment_id}")
        print(f"[INFO] View comment thread at: https://www.youtube.com/watch?v={VIDEO_ID}&lc={comment_id}")
    except Exception as e:
        print(f"[ERROR] Failed to post comment: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
