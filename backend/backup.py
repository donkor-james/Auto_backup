import sys
import os
import datetime
import shutil
import schedule
import time
import logging
import pathlib
import requests
import humanize
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload
from models import db, File, Folder
from app import app
# backup directory to another folder

# with app.app_context():
#     objects = db.session.query(File).all()

#     for obj in objects:
#         obj.file_size = str(obj.file_size) + " KB"

#     db.session.commit()
#     objs = db.session.query(File).all()

#     for obj in objs:
#         print("New\n", obj.file_size, type(obj.file_size))


monitored_folders = {
    "Documents": "OneDrive\\Documents",
    "Downloads": "Downloads",
    "Desktop": "Desktop",
    "Videos": "Videos",
    "Music": "Music"
}
# Upload file and folders to google cloud


def get_folder_size(path):

    total_size = 0

    for item in os.listdir(path):
        item_path = os.path.join(path, item)
        if os.path.isfile(item_path):
            total_size += os.path.getsize(item_path)
        elif os.path.isdir(item_path):
            total_size += get_folder_size(item_path)

    return humanize.naturalsize(total_size)
    # size = sum(os.path.getsize(os.path.join(root, filename))
    #            for root, _, filenames in os.walk(path) for filename in filenames)

    # size = sum(file.stat().st_size for file in pathlib.Path(
    #     path).rglob() if file.is_file())
    # return f"{size}"


def create_upload_folder(backup_file, folder_id, service, actual_path):
    print(backup_file)
    for root, dirs, files in os.walk(backup_file):
        for file in files:
            if os.path.isfile(backup_file+'\\'+file):
                print("code to upload file")
                file_metadata = {
                    'name': file,
                    'parents': [folder_id]
                }

                media = MediaFileUpload(f"{backup_file}\{file}")
                media.chunksize = -1

                upload_file = service.files().create(
                    body=file_metadata, media_body=media, fields='id').execute()

                print(f"Backed up: {file}\nparent_folder: {backup_file} \n")

        for dir in dirs:
            count = count + 1
            print("code to create and upload to folder")

            response = service.files().list(
                q="name = '{}' and mimeType='application/vnd.google-apps.folder'".format(
                    dir),
                spaces='drive').execute()

            if dir not in response['files']:
                file_metadata = {
                    'name': dir,
                    "parents": [folder_id],
                    'mimeType': "application/vnd.google-apps.folder"
                }

                file = service.files().create(body=file_metadata, fields='id').execute()
                parent_folder_id = file.get('id')

            else:
                parent_folder_id = response['files'][dir]['id']

            new_backup = backup_file + "\\" + dir
            actual_path = actual_path + "\\" + dir
#     id = db.Column(db.Integer, primary_key=True)
    # name = db.Column(db.String(100), nullable=False)
    # folder_size = db.Column(db.Integer)
    # parent_id = db.Column(db.String(255), nullable=False)

    #  file_data = {
    #       'name': dir,
    #       'file_size': os.path.getsize(backup_file + '\\' + file),
    #         'file_path': actual_path
    #       }

    #   new_folder = Folder(dir, )

    #    with app.app_context():
    #         db.session.add(new_file)
    #         db.session.commit()
    #         print('saved to database successfully', new_file)

    #     create_upload_folder(new_backup, parent_folder_id, service, )


def upload_res(backup_file, creds, actual_path):
    if os.path.exists("C:\\Users\\Donkor James\\Desktop\\Auto_backup\\drive_credentials\\token.json"):
        creds = Credentials.from_authorized_user_file(
            "C:\\Users\\Donkor James\\Desktop\\Auto_backup\\drive_credentials\\token.json", SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "C:\\Users\\Donkor James\\Desktop\\Auto_backup\\drive_credentials\\credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)

        with open('C:\\Users\\Donkor James\\Desktop\\Auto_backup\\drive_credentials\\token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build("drive", "v3", credentials=creds)

        response = service.files().list(
            q="name = 'BackupFolder' and mimeType='application/vnd.google-apps.folder'",
            spaces='drive').execute()

        if not response['files']:
            file_metadata = {
                'name': 'BackupFolder',
                'mimeType': "application/vnd.google-apps.folder"
            }

            file = service.files().create(body=file_metadata, fields='id').execute()
            folder_id = file.get('id')

        else:
            folder_id = response['files'][0]['id']
            create_upload_folder(backup_file, folder_id, service, actual_path)
        # for file in os.listdir(backup_file):
        #     file_metadata = {
        #         'name': file,
        #         'parents': [folder_id]
        #     }

        #     media = MediaFileUpload(f"{backup_file}\{file}")
        #     media.chunksize = -1

        #     upload_file = service.files().create(
        #         body=file_metadata, media_body=media, fields='id').execute()

        #     print("Backed up: " + file)
    except HttpError as e:
        print("Error: " + str(e))


def copy_to_backup(source, dest, event, home_dir_temp):
    temp_source = source
    event_path = event.src_path
    concat_path = event_path[len(source)+1:]
    files = concat_path.split("\\")
    file = files[0]
    last_file = files[-1]
    temp_source = temp_source + "\\" + file
    dest_dir = dest + '\\' + file

    if os.path.isfile(temp_source):
        if os.path.exists(dest_dir):
            os.remove(dest_dir)
        shutil.copy(temp_source, dest_dir)
        # return "folder copied to: {}".format(dest_dir)
    elif not os.path.isfile(temp_source) and os.path.exists(temp_source):
        if os.path.exists(dest_dir):
            shutil.rmtree(dest_dir)
        shutil.copytree(temp_source, dest_dir)

        # size = get_folder_size()
        # new_folder = Folder(file, )
        # return f'source: {temp_source} \ndest: {dest_dir}'

    for key in monitored_folders.keys():
        if key in event_path:
            with app.app_context():
                folder = db.session.query(Folder).filter_by(name=key).first()
                size = get_folder_size(dest)
                folder.folder_size = size
                db.session.commit()
            break
    return f"{last_file} backup in {dest}"


def on_modified(event):
    backup_path = os.path.expanduser('~')
    backup_path = backup_path + "\OneDrive\Desktop\Pictures\Backup"

    # print(event)
    # msg = copy_to_backup(home_dir, backup_path, event)
    # print(msg)


def on_created(event):
    home_dir = os.path.expanduser('~')
    backup_path = os.path.expanduser('~')
    backup_path = backup_path + "\OneDrive\Desktop\Pictures\Backup"

    for key in monitored_folders.keys():
        if key in event.src_path:
            backup_path = os.path.join(backup_path, key)
            home_dir_temp = home_dir + "\\" + monitored_folders[key]
            if not os.path.exists(backup_path):
                os.mkdir(backup_path)
                size = get_folder_size(backup_path)

                folder_meta = {
                    "name": key,
                    "folder_size": size
                }
                with app.app_context():
                    new_folder = Folder(
                        name=folder_meta["name"], folder_size=folder_meta["folder_size"])

                    db.session.add(new_folder)
                    db.session.commit()

            msg = copy_to_backup(
                home_dir_temp, backup_path, event, home_dir_temp)
            break

    # upload_res(backup_path, creds, event.src_path)


if __name__ == '__main__':
    home_dir = os.path.expanduser('~')
    print(home_dir)
    SCOPES = ["https://www.googleapis.com/auth/drive"]
    creds = None

    folder1 = home_dir + "\\" + monitored_folders["Videos"]
    folder2 = home_dir + "\\" + monitored_folders["Documents"]
    folder3 = home_dir + "\\" + monitored_folders["Downloads"]
    folder4 = home_dir + "\\" + monitored_folders["Desktop"]
    folder5 = home_dir + "\\" + monitored_folders["Music"]

    logging.basicConfig(
        level=logging.INFO, format='%(asctime)s -%(process)d - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    event_handler = LoggingEventHandler()
    event_handler.on_modified = on_modified
    event_handler.on_created = on_created

    folder1_observer = Observer()
    folder1_observer.schedule(event_handler, folder1, recursive=True)
    folder1_observer.start()

    folder2_observer = Observer()
    folder2_observer.schedule(event_handler, folder2, recursive=True)
    folder2_observer.start()

    folder3_observer = Observer()
    folder3_observer.schedule(event_handler, folder3, recursive=True)
    folder3_observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        folder1_observer.stop()
        folder2_observer.stop()
        folder3_observer.stop()

        folder1_observer.join()
        folder2_observer.join()
        folder3_observer.join()
