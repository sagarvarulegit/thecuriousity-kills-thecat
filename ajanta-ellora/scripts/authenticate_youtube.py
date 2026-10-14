#!/usr/bin/env python3
"""
YouTube OAuth 2.0 Desktop Authenticator
Generates token.json for automated YouTube Data API uploads.
"""

import sys
import json
import urllib.parse
from http.server import HTTPServer, BaseHTTPRequestHandler
from pathlib import Path
from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = [
    "https://www.googleapis.com/auth/youtube.upload",
    "https://www.googleapis.com/auth/youtube.force-ssl",
    "https://www.googleapis.com/auth/youtube"
]

WORKSPACE_ROOT = Path(__file__).resolve().parent.parent.parent
CLIENT_SECRETS_PATH = WORKSPACE_ROOT / "client_secret.json"
TOKEN_PATH = WORKSPACE_ROOT / "token.json"

AUTH_CODE = None

class OAuthCallbackHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        global AUTH_CODE
        parsed = urllib.parse.urlparse(self.path)
        params = urllib.parse.parse_qs(parsed.query)
        if "code" in params:
            AUTH_CODE = params["code"][0]
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            success_html = """
            <html>
            <body style="font-family: sans-serif; text-align: center; padding: 50px; background: #0A0A0C; color: #F7E7CE;">
                <h1 style="color: #D4AF37;">Authentication Successful!</h1>
                <p>Google OAuth credentials have been authorized for <strong>The Curiosity Kills The Cat</strong>.</p>
                <p>You can close this browser tab and return to the terminal. The automated uploader will now proceed!</p>
            </body>
            </html>
            """
            self.wfile.write(success_html.encode("utf-8"))
        else:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b"Authorization failed or code missing.")

    def log_message(self, format, *args):
        # Suppress noisy HTTP server logs
        return

def main():
    if not CLIENT_SECRETS_PATH.exists():
        print(f"[ERROR] client_secret.json not found at: {CLIENT_SECRETS_PATH}")
        sys.exit(1)

    port = 8080
    redirect_uri = f"http://127.0.0.1:{port}/"

    flow = InstalledAppFlow.from_client_secrets_file(
        str(CLIENT_SECRETS_PATH),
        scopes=SCOPES,
        redirect_uri=redirect_uri
    )

    auth_url, _ = flow.authorization_url(prompt="consent", access_type="offline")

    auth_url_file = WORKSPACE_ROOT / "ajanta-ellora" / "supercut" / "staging" / "auth_url.txt"
    auth_url_file.parent.mkdir(parents=True, exist_ok=True)
    auth_url_file.write_text(auth_url, encoding="utf-8")

    print("\n===================================================================", flush=True)
    print("  YOUTUBE OAUTH 2.0 AUTHENTICATION SETUP", flush=True)
    print("===================================================================", flush=True)
    print("\n1. Opening your web browser for Google Account Sign-In...", flush=True)
    print("\nIf your browser does not open automatically, copy and paste this link:", flush=True)
    print(f"\n{auth_url}\n", flush=True)
    print("===================================================================", flush=True)
    print(f"Waiting for authorization on {redirect_uri}...", flush=True)

    # Start local server to receive callback
    server = HTTPServer(("127.0.0.1", port), OAuthCallbackHandler)
    while AUTH_CODE is None:
        server.handle_request()

    print("\n[AUTH] Authorization code received! Exchanging for tokens...")
    flow.fetch_token(code=AUTH_CODE)
    creds = flow.credentials

    with open(TOKEN_PATH, "w", encoding="utf-8") as f:
        f.write(creds.to_json())

    print(f"[SUCCESS] Credentials permanently saved to: {TOKEN_PATH}")
    print("You can now run the automated uploader without signing in again!")

if __name__ == "__main__":
    main()
