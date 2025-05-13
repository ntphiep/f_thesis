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
SCOPES = ['https://www.googleapis.com/auth/drive.readonly']
CREDENTIALS_PATH = 'credentials.json'
TOKEN_PATH = 'token.json'
FOLDER_NAME = 'style_transfer_paraphrase'

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

def get_folder_id(service, folder_name):
    """Gets the ID of a folder with the given name.
    """
    try:
        results = service.files().list(
            q=f"name='{folder_name}' and mimeType='application/vnd.google-apps.folder'",
            fields="nextPageToken, files(id, name)").execute()
        items = results.get('files', [])
        if not items:
            print(f'No folder found with name: {folder_name}.')
            return None
        return items[0]['id']
    except HttpError as error:
        print(f'An error occurred: {error}')
        return None

def list_files_recursive(service, folder_id, indent=0):
    """Lists all files and folders inside the given folder recursively.
    """
    try:
        results = service.files().list(
            q=f"'{folder_id}' in parents",
            fields="nextPageToken, files(id, name, mimeType)").execute()
        items = results.get('files', [])

        for item in items:
            print("  " * indent + f"- {item['name']} ({item['id']}) - {item['mimeType']}")
            if item['mimeType'] == 'application/vnd.google-apps.folder':
                list_files_recursive(service, item['id'], indent + 1)

    except HttpError as error:
        print(f'An error occurred: {error}')

def main():
    creds = get_credentials()

    try:
        service = build('drive', 'v3', credentials=creds)

        folder_id = get_folder_id(service, FOLDER_NAME)
        if folder_id:
            print(f"Contents of folder '{FOLDER_NAME}':")
            list_files_recursive(service, folder_id)
        else:
            print(f"Folder '{FOLDER_NAME}' not found.")

    except HttpError as error:
        print(f'An error occurred: {error}')

if __name__ == '__main__':
    main()
