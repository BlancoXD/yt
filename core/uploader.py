import pickle
import os
import json
from pathlib import Path
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]

def get_authenticated_service(client_secrets_file):
    credentials = None
    token_path = Path("token.pickle")

    if token_path.exists():
        with open(token_path, "rb") as token:
            credentials = pickle.load(token)

    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(client_secrets_file, SCOPES)
            credentials = flow.run_console()

        with open(token_path, "wb") as token:
            pickle.dump(credentials, token)

    return build("youtube", "v3", credentials=credentials)

def upload_to_youtube(video_path, thumbnail_path, config):
    print("[Uploader] Uploading video...")

    youtube = get_authenticated_service(config["youtube"]["client_secrets_file"])

    title = Path(video_path).stem.replace("_", " ").capitalize()
    description = f"This video was generated automatically about: {title}"

    request_body = {
        "snippet": {
            "title": title,
            "description": description,
            "tags": ["AI", "Automation", "YouTube", "Faceless"],
            "categoryId": "22"
        },
        "status": {
            "privacyStatus": "public"
        }
    }

    media_file = MediaFileUpload(video_path)
    video_response = youtube.videos().insert(
        part="snippet,status",
        body=request_body,
        media_body=media_file
    ).execute()

    print(f"[Uploader] Video uploaded: https://youtu.be/{video_response['id']}")

    if thumbnail_path:
        youtube.thumbnails().set(
            videoId=video_response["id"],
            media_body=MediaFileUpload(thumbnail_path)
        ).execute()
        print("[Uploader] Thumbnail uploaded.")

    return video_response["id"]
import pickle
import os
import json
from pathlib import Path
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]

def get_authenticated_service(client_secrets_file):
    credentials = None
    token_path = Path("token.pickle")

    if token_path.exists():
        with open(token_path, "rb") as token:
            credentials = pickle.load(token)

    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(client_secrets_file, SCOPES)
            credentials = flow.run_console()

        with open(token_path, "wb") as token:
            pickle.dump(credentials, token)

    return build("youtube", "v3", credentials=credentials)

def upload_to_youtube(video_path, thumbnail_path, config):
    print("[Uploader] Uploading video...")

    youtube = get_authenticated_service(config["youtube"]["client_secrets_file"])

    title = Path(video_path).stem.replace("_", " ").capitalize()
    description = f"This video was generated automatically about: {title}"

    request_body = {
        "snippet": {
            "title": title,
            "description": description,
            "tags": ["AI", "Automation", "YouTube", "Faceless"],
            "categoryId": "22"
        },
        "status": {
            "privacyStatus": "public"
        }
    }

    media_file = MediaFileUpload(video_path)
    video_response = youtube.videos().insert(
        part="snippet,status",
        body=request_body,
        media_body=media_file
    ).execute()

    print(f"[Uploader] Video uploaded: https://youtu.be/{video_response['id']}")

    if thumbnail_path:
        youtube.thumbnails().set(
            videoId=video_response["id"],
            media_body=MediaFileUpload(thumbnail_path)
        ).execute()
        print("[Uploader] Thumbnail uploaded.")

    return video_response["id"]
