import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload
import analysis as A
from paramiko import SSHClient, AutoAddPolicy
# Replace with your FTP credentials or delete
import ftp_login
import datetime

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/drive"]
gdrive_destination_folder_id = "1zZjkRWWPLLI5-Xqet1RpJ1NwtgSfUV6s" # User specific

def upload_file_to_gdrive(source_file, dest_name, dest_folder=gdrive_destination_folder_id):
  """Uploads a file to a specified folder in Google Drive"""

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
  
def upload_file_SFTP(source_file, dest_filename, host=ftp_login.host, port=ftp_login.port, username=ftp_login.username, password=ftp_login.password, path=ftp_login.path):
    """Uploads a file to an FTP server using SFTP. Uses FTP credentials in ftp_login.py by default."""

    with SSHClient() as ssh:
       print("SFTP connecting")
       ssh.set_missing_host_key_policy(AutoAddPolicy())
       ssh.connect(hostname=host,port=port,username=username,password=password)
       with ssh.open_sftp() as sftp:
          sftp.chdir(path)
          files = sftp.put(localpath=source_file, remotepath=dest_filename)
        
    return files
          

def create_chart_and_upload(chart_type: A.PlotTypes, chart_args: list=[]):
    """Creates a chart and uploads it"""

    print(f"Creating Chart {chart_type.name}")

    if chart_type == A.PlotTypes.WEEKDAY_FIXED_LINE:
       if not chart_args or chart_args[0] not in [0,1,2,3,4,5,6]:
          print(f"{chart_type.name} requires 1 argument: WEEKDAY[0-6]")
          return False    
       source_file = A.fixed_linechart_for_weekday(int(chart_args[0]))
    elif chart_type == A.PlotTypes.DATE_FIXED_LINE:
       if not chart_args:
          print(f"{chart_type.name} requires 1 argument: 'YYYY-MM-DD'")
          return False
       source_file = A.fixed_linechart_date(chart_args[0])
       dest_file = "date.png"
    elif chart_type == A.PlotTypes.OVERLAYED_WEEKDAYS_FIXED_LINE:
       source_file = A.overlay_weekdays()
    elif chart_type == A.PlotTypes.TOTAL_AVERAGES:
       source_file = A.total_averages()
    else:
       print(f"Invalid Chart Type {chart_type}")
       return False
    
    gdrive_uploaded = upload_file_to_gdrive(source_file, source_file, gdrive_destination_folder_id)
    ftp_uploaded = upload_file_SFTP(source_file, dest_file) if dest_file else upload_file_SFTP(source_file, source_file)
    return (gdrive_uploaded, ftp_uploaded)

def nightly_upload(now=datetime.datetime.now()):
   ow_uploaded = create_chart_and_upload(A.PlotTypes.OVERLAYED_WEEKDAYS_FIXED_LINE)
   fl_uploaded = create_chart_and_upload(A.PlotTypes.WEEKDAY_FIXED_LINE, [now.weekday()])
   ifl_uploaded = create_chart_and_upload(A.PlotTypes.DATE_FIXED_LINE, [now.strftime('%Y-%m-%d')])
   ta_uploaded = create_chart_and_upload(A.PlotTypes.TOTAL_AVERAGES)
   return (ow_uploaded, fl_uploaded, ifl_uploaded, ta_uploaded)

if __name__ == "__main__":
   nightly_upload()