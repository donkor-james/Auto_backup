import sys
import os
import json
import io
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
from googleapiclient.http import MediaIoBaseDownload
from models import db, File, Folder, User
from app import app


monitored_folders = {
    "Documents": "OneDrive\\Documents",
    # "Downloads": "Downloads",
    "Desktop": "Desktop",
    "Videos": "Videos",
    "Music": "Music"
}


backup_intervals = {
    "Daily": 1,
    "Weekly": 7,
    "Monthly": 30
}
last_interval = None

file_path = "C:\\Users\\Donkor James\\Auto_backup2\\Auto_backup\\userData.json"


def list_files(service, folder_id):
    query = f"'{folder_id}' in parents"
    results = service.files().list(q=query).execute()
    items = results.get('files', [])
    return items


def download_file(service, file_id, file_name):
    request = service.files().get_media(fileId=file_id)
    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
    fh.seek(0)

    with open(file_name, 'wb') as f:
        f.write(fh.read())
        f.close()


def restore_data():
    global drive_backup_id
    flow = InstalledAppFlow.from_client_secrets_file(
        'credentials.json', SCOPES)
    creds = flow.run_local_server(port=0)
    service = build('drive', 'v3', credentials=creds)

    items = list_files(service, drive_backup_id)

    with app.app_context():
        files = File.query.all()
    for item in items:
        if item['mimeType'] == 'application/vnd.google-apps.folder':
            restore_data(item['id'])
        else:
            return


def backup_scheduler():
    global last_interval
    global user_id
    global drive_backup_id
    global credens
    dest2 = os.path.expanduser("~")
    backup_path = dest2 + "\\backup"
    backup_folder_temp2 = dest2
    backupParent2 = dest2

    with app.app_context():
        with open(file_path, "r") as file:
            login_credentials = json.load(file)

            user = User.query.get(login_credentials["id"])

            backup_schdule = user.backup_schedule

            if backup_schdule and backup_schdule != "On Arrival" and backup_schdule != last_interval:
                schedule.clear("task")
                interval = backup_intervals[backup_schdule]
                print(f"---- Changing scheduler to {interval} days----")
                schedule.every(interval).days.do(lambda: upload_res(
                    credens, backup_path, backup_path, backup_path)).tag("task")
                last_interval = backup_schdule


def get_folder_size(path):

    total_size = 0

    for item in os.listdir(path):
        item_path = os.path.join(path, item)
        if os.path.isfile(item_path):
            total_size += os.path.getsize(item_path)
        elif os.path.isdir(item_path):
            total_size += get_folder_size(item_path)
    return total_size


def to_bytes(size):
    units = {
        "kb": 1024,
        "mb": 1024 ** 2,
        "gb": 1024 ** 3,
        "tb": 1024 ** 4
    }

    for unit in units.keys():
        if isinstance(size, str):
            size_list = size.split(" ")
            size_unit = size_list[1]
            if size_unit.lower() == unit:
                number = size[: - len(unit)]
                return int(float(number) * units[unit])
            elif size_unit.lower == "bytes":
                return int(size_list[0])
    if size != None and isinstance(size, str):
        size_list = size.split(" ")
        return int(size_list[0])
    elif size != None and isinstance(size, int):
        return size
    else:
        return 0


def create_upload_folder(folder_id, service, actual_path, backup_temp):
    global user_id

    for root, dirs, files in os.walk(backup_temp):
        for file in files:
            if os.path.isfile(backup_temp+'\\'+file):
                file_metadata = {
                    'name': file,
                    'parents': [folder_id]
                }

                media = MediaFileUpload(f"{backup_temp}\{file}")
                media.chunksize = -1

                upload_file = service.files().create(
                    body=file_metadata, media_body=media, fields='id').execute()

                print(f"\n\n--- Backed up:{file}  To: Google Drive ---\n")

                file_size = os.path.getsize(backup_temp+'\\'+file)
                with app.app_context():
                    new_file = File(name=file, file_size=file_size,
                                    file_path=backup_temp+"\\"+file)
                    db.session.add(new_file)
                    user = User.query.get(user_id)
                    total_data = user.total_data
                    total_bytes = to_bytes(total_data)
                    new_size = to_bytes(file_size)
                    total_bytes = total_bytes + new_size

                    user.total_data = humanize.naturalsize(total_bytes)
                    db.session.commit()
                    user = User.query.get(user_id)

        for dir in dirs:
            inDrive = False

            response = service.files().list(
                q="name = '{}' and mimeType='application/vnd.google-apps.folder'".format(
                    dir),
                spaces='drive').execute()

            for folders in response['files']:
                if dir == folders["name"]:
                    parent_folder_id = folders["id"]
                    inDrive = True
                    break
                else:
                    inDrive = False
            if not inDrive:
                file_metadata = {
                    'name': dir,
                    "parents": [folder_id],
                    'mimeType': "application/vnd.google-apps.folder"
                }

                file = service.files().create(body=file_metadata, fields='id').execute()
                parent_folder_id = file.get('id')

            new_backup = backup_temp + "\\" + dir
            actual_path = actual_path + "\\" + dir

            create_upload_folder(parent_folder_id, service,
                                 actual_path, new_backup)

            shutil.rmtree(new_backup)


def upload_res(credens, actual_path, backupParent, backup_temp):
    global user_id
    global drive_backup_id

    if os.path.exists("C:\\Users\\Donkor James\\Auto_backup2\\Auto_backup\\drive_credentials\\token.json"):
        credens = Credentials.from_authorized_user_file(
            "C:\\Users\\Donkor James\\Auto_backup2\\Auto_backup\\drive_credentials\\token.json", SCOPES)

    if not credens or not credens.valid:
        if credens and credens.expired and credens.refresh_token:
            credens.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "C:\\Users\\Donkor James\\Auto_backup2\\Auto_backup\\drive_credentials\\credentials.json", SCOPES)
            credens = flow.run_local_server(port=0)

        with open('C:\\Users\\Donkor James\\Auto_backup2\\Auto_backup\\drive_credentials\\token.json', 'w') as token:
            token.write(credens.to_json())

    try:
        service = build("drive", "v3", credentials=credens)
        with app.app_context():
            user = User.query.get(user_id)
            username = user.name
            password = user.password
            folder_name = username + "_" + str(password)
            response = service.files().list(
                q=f"name = '{folder_name}' and mimeType='application/vnd.google-apps.folder'",
                spaces='drive').execute()

            if not response['files']:
                file_metadata = {
                    'name': folder_name,
                    'mimeType': "application/vnd.google-apps.folder"
                }

                file = service.files().create(body=file_metadata, fields='id').execute()
                folder_id = file.get('id')
                drive_backup_id = folder_id

            else:
                folder_id = response['files'][0]['id']

            create_upload_folder(folder_id,
                                 service, actual_path, backup_temp)

    except HttpError as e:
        print("Error: " + str(e))


def copy_to_backup(source, dest, event, backup_folder_temp, backupParent):
    temp_source = source
    event_path = event.src_path
    concat_path = event_path[len(source)+1:]
    files = concat_path.split("\\")
    file = files[0]
    last_file = files[-1]
    temp_source = temp_source + "\\" + file
    dest_dir = dest + '\\' + file
    global user_id

    if os.path.isfile(temp_source):
        if os.path.exists(dest_dir):
            os.remove(dest_dir)
        shutil.copy(temp_source, dest_dir)
    elif not os.path.isfile(temp_source) and os.path.exists(temp_source):
        if os.path.exists(dest_dir):
            shutil.rmtree(dest_dir)
        shutil.copytree(temp_source, dest_dir)

    for key in monitored_folders.keys():
        if key in event_path:
            with open(file_path, "r") as file:
                login_credentials = json.load(file)

                with app.app_context():
                    folder = db.session.query(
                        Folder).filter_by(name=key).first()

                    folders = db.session.query(
                        Folder).filter_by(name=key).first()
                    size = get_folder_size(dest)
                    folder_size = to_bytes(folder.folder_size)
                    total_folder_size = size + folder_size
                    total_folder_size = humanize.naturalsize(total_folder_size)
                    folder.folder_size = total_folder_size

                    user_id = login_credentials["id"]
                    user = User.query.get(user_id)
                    db.session.commit()

                    backup_schdule = user.backup_schedule
                    if backup_schdule == "On Arrival":
                        upload_res(credens, event.src_path,
                                   backupParent, backup_folder_temp)
            break

        # size = get_folder_size()
        # new_folder = Folder(file, )
        # return f'source: {temp_source} \ndest: {dest_dir}'
    return f"{last_file} backup in {dest}"


def on_modified(event):
    backup_path = os.path.expanduser('~')
    backup_path = backup_path + "Backup"


def on_created(event):
    home_dir = os.path.expanduser('~')
    home_dir_temp = ""
    backup_path = os.path.expanduser('~')
    backup_path = backup_path + "\Backup"
    backup_path_temp = backup_path
    dest2 = ""
    credens2 = ""
    event_path2 = event.src_path,
    backupParent2 = ""
    backup_folder_temp2 = ""

    for key in monitored_folders.keys():
        if key in event.src_path:
            backup_path = os.path.join(backup_path, key)
            home_dir_temp = home_dir + "\\" + monitored_folders[key]
            if not os.path.exists(backup_path):
                os.mkdir(backup_path)

                with app.app_context():
                    size = get_folder_size(backup_path)
                    new_size = humanize.naturalsize(size)

                    folder_meta = {
                        "name": key,
                        "folder_size": new_size
                    }
                    new_folder = Folder(
                        name=folder_meta["name"], folder_size=folder_meta["folder_size"])

                    db.session.add(new_folder)
                    db.session.commit()
                    music = Folder.query.all()

            msg = copy_to_backup(
                home_dir_temp, backup_path, event, backup_path_temp, key)


if __name__ == '__main__':
    home_dir = os.path.expanduser('~')
    SCOPES = ["https://www.googleapis.com/auth/drive"]
    credens = None
    user_id = None
    drive_backup_id = None

    print("THis is a loop")
    folder1 = home_dir + "\\" + monitored_folders["Videos"]
    folder2 = home_dir + "\\" + monitored_folders["Documents"]
    # folder3 = home_dir + "\\" + monitored_folders["Downloads"]
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

    # folder3_observer = Observer()
    # # folder3_observer.schedule(event_handler, folder3, recursive=True)
    # folder3_observer.start()

    folder4_observer = Observer()
    folder4_observer.schedule(event_handler, folder4, recursive=True)
    folder4_observer.start()

    folder5_observer = Observer()
    folder5_observer.schedule(event_handler, folder5, recursive=True)
    folder5_observer.start()
    try:
        while True:
            schedule.run_pending()
            backup_scheduler()
            time.sleep(1)
    except KeyboardInterrupt:
        folder1_observer.stop()
        folder2_observer.stop()
        # folder3_observer.stop()
        folder4_observer.stop()
        folder5_observer.stop()

        folder1_observer.join()
        folder2_observer.join()
        # folder3_observer.join()
        folder4_observer.join()
        folder5_observer.join()
