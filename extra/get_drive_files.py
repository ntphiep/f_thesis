import os
import io

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.auth.transport.requests import Request
from google.oauth2 import id_token
from google.auth.transport import requests
from googleapiclient.http import MediaIoBaseDownload

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/drive']
CREDENTIALS_PATH = 'credentials.json'
TOKEN_PATH = 'token.json'

def get_credentials():
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists(TOKEN_PATH):
        creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            from google_auth_oauthlib.flow import InstalledAppFlow
            flow = InstalledAppFlow.from_client_secrets_file(
                CREDENTIALS_PATH, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(TOKEN_PATH, 'w') as token:
            token.write(creds.to_json())
    return creds

def list_files():
    """Lists all the files in the user's Google Drive.
    """
    creds = get_credentials()

    try:
        service = build('drive', 'v3', credentials=creds)

        # Call the Drive v3 API
        results = service.files().list(
            pageSize=1000, # You can increase this to retrieve more files per page
            q="mimeType='application/vnd.google-apps.folder'",
            fields="nextPageToken, files(id, name, mimeType)").execute()
        items = results.get('files', [])

        if not items:
            print('No folders found.')
            return

        print('Folders:')
        for item in items:
            print(f"{item['name']} ({item['id']}) - {item['mimeType']}")

        # Handle pagination if there are more than 1000 files
        next_page_token = results.get('nextPageToken')
        while next_page_token:
            results = service.files().list(
                q="mimeType='application/vnd.google-apps.folder'",
                pageSize=1000,
                fields="nextPageToken, files(id, name, mimeType)",
                pageToken=next_page_token).execute()
            items = results.get('files', [])
            for item in items:
                print(f"{item['name']} ({item['id']}) - {item['mimeType']}")
            next_page_token = results.get('nextPageToken')

    except HttpError as error:
        print(f'An error occurred: {error}')

if __name__ == '__main__':
    list_files()
