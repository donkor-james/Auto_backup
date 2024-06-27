import sys
import os
import datetime
import shutil
import schedule
import time
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler
import logging
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload
# backup directory to another folder


monitored_folders = ["Document"]
# Upload file and folders to google cloud


def upload_res(backup_file, creds):
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "C:\\Users\\Donkor James\\OneDrive\\Documents\\mini_project\\backend\\credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)

        with open('C:\\Users\\Donkor James\\OneDrive\\Documents\\mini_project\\token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build("drive", "v3", credentials=creds)

        response = service.files().list(
            q="name = 'BackupFolder' and mimeType='application/vnd.google-apps.folder'",
            spaces='drive').execute()

        if not response['files']:
            file_metadata = {
                'name': 'BackupFolder',
                'mimeType': "application/application/vnd.google-apps.folder"
            }

            file = service.files().create(body=file_metadata, fields='id').execute()
            folder_id = file.get('id')

        else:
            folder_id = response['files'][0]['id']

        for file in os.listdir(backup_file):
            file_metadata = {
                'name': file,
                'parents': [folder_id]
            }

            media = MediaFileUpload(f"{backup_file}\{file}")
            media.chunksize = -1
            media.resumable = True

            upload_file = service.files().create(
                body=file_metadata, media_body=media, fields='id').execute()

            print("Backed up: " + file)
    except HttpError as e:
        print("Error: " + str(e))


def copy_to_backup(source, dest, event):
    temp_source = source
    event_path = event.src_path
    concat_path = event_path[len(home_dir)+1:]
    files = concat_path.split("\\")
    print(files[0])
    file = files[0]
    temp_source = temp_source + "\\" + file
    print(file)
    dest_dir = dest + '\\' + file

    if os.path.isfile(temp_source):
        if os.path.exists(dest_dir):
            os.remove(dest_dir)
        shutil.copy(temp_source, dest_dir)
        return "folder copied to: {}".format(dest_dir)
    elif not os.path.isfile(temp_source) and os.path.exists(temp_source):
        if os.path.exists(dest_dir):
            shutil.rmtree(dest_dir)
        shutil.copytree(temp_source, dest_dir)
        return f'source: {temp_source} \ndest: {dest_dir}'


def on_modified(event):
    backup_path = os.path.expanduser('~')
    backup_path = backup_path + "\OneDrive\Desktop\Pictures\Backup"

    # msg = copy_to_backup(home_dir, backup_path, event)
    # print(msg)


def on_created(event):
    backup_path = os.path.expanduser('~')
    backup_path = backup_path + "\OneDrive\Desktop\Pictures\Backup"

    msg = copy_to_backup(home_dir, backup_path, event)
    print(msg)

    upload_res(backup_path, creds)


if __name__ == '__main__':
    home_dir = os.path.expanduser('~')
    home_dir = home_dir + '\OneDrive\Documents'
    SCOPES = ["https://www.googleapis.com/auth/drive"]
    creds = None

    logging.basicConfig(
        level=logging.INFO, format='%(asctime)s -%(process)d - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    event_handler = LoggingEventHandler()
    # event_handler.on_modified = on_modified
    event_handler.on_created = on_created
    observer = Observer()
    observer.schedule(event_handler, home_dir, recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        observer.join()
