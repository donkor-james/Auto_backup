import sys
import os
import json
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
from models import db, File, Folder, User
from app import app

backup_intervals = {
    "Daily": 1,
    "Weekly": 7,
    "Monthly": 30
}

monitored_folders = {
    "Documents": "OneDrive\\Documents",
    # "Downloads": "Downloads",
    "Desktop": "Desktop",
    "Videos": "Videos",
    "Music": "Music"
}

last_interval = None

file_path = "C:\\Users\\Donkor James\\Desktop\\Auto_backup2\\Auto_backup\\userData.json"


def do_smn():
    print(f"Doing task on {last_interval} basics")


def backup_scheduler():
    global last_interval
    with app.app_context():
        with open(file_path, "r") as file:
            login_credentials = json.load(file)
            # print(login_credentials, "login_cred")

            user = User.query.get(login_credentials["id"])

            backup_schdule = user.backup_schedule
            # print()
            # intervall = backup_intervals.get(backup_schdule, None)
            if backup_schdule and backup_schdule != "On Arrival" and backup_schdule != last_interval:
                schedule.clear("task")
                interval = backup_intervals[backup_schdule]
                print(f"---- Changing scheduler to {interval} seconds----")
                schedule.every(interval).days.do(upload_res).tag("task")
                last_interval = backup_schdule

                # print(f"updated task schedule to run every {last_interval}")
# backup directory to another folder

# with app.app_context():
#     objects = db.session.query(File).all()

#     for obj in objects:
#         obj.file_size = str(obj.file_size) + " KB"

#     db.session.commit()
#     objs = db.session.query(File).all()

#     for obj in objs:
#         print("New\n", obj.file_size, type(obj.file_size))


# Upload file and folders to google cloud


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
        if size:
            size_list = size.split(" ")
            size_unit = size_list[1]
            print(size, size_unit.lower())
            if size_unit.lower() == unit:
                number = size[: - len(unit)]
                return int(float(number) * units[unit])
            else:
                return int(size_list[0])
        else:
            return 0
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

    for key in monitored_folders.keys():
        if key in event_path:
            with open(file_path, "r") as file:
                login_credentials = json.load(file)
                # print(login_credentials, "login_cred")

                with app.app_context():
                    folder = db.session.query(
                        Folder).filter_by(name=key).first()
                    size = get_folder_size(dest)
                    size = humanize.naturalsize(size)
                    folder.folder_size = size

                    user = User.query.get(login_credentials["id"])
                    total_data = user.total_data
                    total_bytes = to_bytes(total_data)
                    new_size = to_bytes(size)
                    total_bytes = total_bytes + new_size
                    # parsed_data = humanize.pa total_data
                    print(total_bytes)
                    user.total_data = humanize.naturalsize(total_bytes)
                    db.session.commit()
                    # user = db.session
            break

        # size = get_folder_size()
        # new_folder = Folder(file, )
        # return f'source: {temp_source} \ndest: {dest_dir}'
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

            msg = copy_to_backup(
                home_dir_temp, backup_path, event, home_dir_temp)
            break

        with app.app_context():
            size = get_folder_size(backup_path)
            new_size = humanize.naturalsize(size)

            folder_meta = {
                "name": key,
                "folder_size": new_size
            }
            new_folder = Folder(
                name=folder_meta["name"], folder_size=folder_meta["folder_size"])

            with open(file_path, "r") as file:
                login_credentials = json.load(file)
                print(login_credentials, "login_cred")

                user = User.query.get(login_credentials["id"])
                # user_Total_data = user.total_data

                # user_Total_data = to_bytes(user_Total_data)
                # print(size, user_Total_data)
                # user_Total_data = humanize.naturalsize(size+user_Total_data)
                # user.total_data = user_Total_data

                # db.session.commit()
            backup_schdule = user.backup_schedule
            if backup_schdule == "On Arrival":
                print(f"backing {event.src_path} on arrival")
                # upload_res(backup_path, creds, event.src_path)


if __name__ == '__main__':
    home_dir = os.path.expanduser('~')
    print(home_dir)
    SCOPES = ["https://www.googleapis.com/auth/drive"]
    creds = None

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

    folder3_observer = Observer()
    folder3_observer.schedule(event_handler, folder5, recursive=True)
    folder3_observer.start()

    try:
        while True:
            schedule.run_pending()
            time.sleep(1)
            backup_scheduler()
    except KeyboardInterrupt:
        folder1_observer.stop()
        folder2_observer.stop()
        folder3_observer.stop()

        folder1_observer.join()
        folder2_observer.join()
        folder3_observer.join()
print(type(""))
