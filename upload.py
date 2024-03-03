import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/drive"]
destination_folder_id = "1zZjkRWWPLLI5-Xqet1RpJ1NwtgSfUV6s"

def upload_file(source_file, dest_name, dest_folder=destination_folder_id):
  creds = None
  if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
          "credentials.json", SCOPES
      )
      creds = flow.run_local_server(port=0)
    with open("token.json", "w") as token:
      token.write(creds.to_json())

  try:
    service = build("drive", "v3", credentials=creds)
    results = service.files().list(pageSize=1,fields="files(id)",q="'" + dest_folder + "' in parents and trashed=false and name='" + dest_name + "'").execute()
    files = results.get("files", [])
    media = MediaFileUpload(source_file, mimetype="image/png")
    # If file already exists, update it
    if files != []:
        print(files)
        file_metadata = {}
        file = service.files().update(fileId=files[0]["id"], body=file_metadata, media_body=media, fields="id").execute()
        print(f'File ID: {file.get("id")}')
    # Else create new file
    else:
        file_metadata = {"name": dest_name, "parents": [dest_folder]}
        file = service.files().create(body=file_metadata, media_body=media, fields="id").execute()
        print(f'File ID: {file.get("id")}')
    
  except HttpError as error:
    print(f"An error occurred: {error}")



