import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload
import analysis as A

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/drive"]
destination_folder_id = "1zZjkRWWPLLI5-Xqet1RpJ1NwtgSfUV6s" # User specific

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
        return True
    # Else create new file
    else:
        file_metadata = {"name": dest_name, "parents": [dest_folder]}
        file = service.files().create(body=file_metadata, media_body=media, fields="id").execute()
        print(f'File ID: {file.get("id")}')
        return True
    
  except HttpError as error:
    print(f"An error occurred: {error}")
    return False

def create_chart_and_upload(chart_type: A.ChartTypes, chart_args: list=[]):
    print(f"Creating Chart {chart_type.name}")

    if chart_type == A.ChartTypes.WEEKDAY_FIXED_LINE:
       if not chart_args or chart_args[0] not in [0,1,2,3,4,5,6]:
          print(f"{chart_type.name} requires 1 argument: WEEKDAY[0-6]")
          return False    
       source_file = A.fixed_linechart_for_weekday(int(chart_args[0]))
    elif chart_type == A.ChartTypes.DATE_FIXED_LINE:
       if not chart_args:
          print(f"{chart_type.name} requires 1 argument: 'YYYY-MM-DD'")
          return False
       source_file = A.fixed_linechart_date(chart_args[0])
    elif chart_type == A.ChartTypes.OVERLAYED_WEEKDAYS_FIXED_LINE:
       source_file = A.overlay_weekdays()
    elif chart_type == A.ChartTypes.TOTAL_AVERAGES:
       source_file = A.total_averages()
    else:
       print(f"Invalid Chart Type {chart_type}")
       return False
    
    return upload_file(source_file, source_file, destination_folder_id)


