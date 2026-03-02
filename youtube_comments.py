from googleapiclient.discovery import build
import gspread
from google.oauth2.service_account import Credentials

API_KEY = "API_KEY_HERE"
VIDEO_ID = "VIDEO_ID_HERE"
SHEET_ID = "YOUR_SHEET_ID_HERE"

scopes = ["https://www.googleapis.com/auth/spreadsheets"]
creds = Credentials.from_service_account_file("credentials.json", scopes=scopes)
gc = gspread.authorize(creds)
sheet = gc.open_by_key(SHEET_ID).sheet1

yt = build("youtube", "v3", developerKey=API_KEY)
comments, token = [], None

while True:
    r = yt.commentThreads().list(
        part="snippet", videoId=VIDEO_ID, maxResults=100, pageToken=token
    ).execute()
    for i in r["items"]:
        comments.append([i["snippet"]["topLevelComment"]["snippet"]["textDisplay"]])
    token = r.get("nextPageToken")
    if not token:
        break

sheet.append_rows(comments)
print("All comments saved to Google Sheet!")