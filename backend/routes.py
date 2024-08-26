import os
import json
from flask import request, jsonify, Blueprint
from models import db, File, Folder, User

api_routes = Blueprint('api', __name__)
userId = 1
user2 = {
    "name": '',
    "backup_schedule": '',
    "backedup_at": '',
    "restore_path": '',
    "password": '',
    "isFirstTime": True,
    "total_data": ''
}

file_path = "C:\\Users\\Donkor James\\Auto_backup2\\Auto_backup\\userData.json"


@api_routes.route('/files', methods=['GET'])
def get_file():
    files = File.query.all()
    return jsonify({'files': [{'id': file.id, 'name': file.name, 'file_size': file.file_size, 'file_type': file.file_type, 'file_path': file.file_path} for file in files]})


# Create a new file
@api_routes.route('/file', methods=['POST'])
def create_file():
    data = request.json
    new_file = File(name=data['name'], file_size=data['file_size'],
                    file_type=data['file_type'], file_path=data['file_path'])

    db.session.add(new_file)
    db.session.commit()

    return jsonify({'file': {'id': new_file.id, 'name': new_file.name, 'filesize': new_file.file_size, 'file_type': new_file.file_type, 'filepath': new_file.file_path}})


# Update an existing file
@api_routes.route('/files/<int:file_id>', methods=['PUT'])
def update_file(file_id):
    data = request.json
    file = File.query.get(file_id)
    if not file:
        return jsonify({'error': 'File not found'})

    data = request.json
    file.name = data.get('name', file.name)
    file.file_size = data.get('file_size', file.file_size)
    file.file_type = data.get('file_type', file.file_type)
    file.file_path = data.get('file_path', file.file_path)

    db.session.commit()
    return jsonify({'file': {'id': file.id, 'name': file.name, 'filesize': file.file_size, 'file_type': file.file_type, 'file_path': file.file_path}})

# Delete a file


@api_routes.route('/files/<file_id>', methods=['DELETE'])
def delete_file(file_id):
    file = File.query.get(file_id)
    if not file:
        return jsonify({'error: File not found'})

    db.session.delete(file)
    db.session.commit()

    return jsonify({'result': True})


@api_routes.route('/folders', methods=['GET'])
def get_folder():
    folders = Folder.query.all()
    return jsonify({'folders': [{'id': folder.id, 'name': folder.name, 'folder_size': folder.folder_size} for folder in folders]})


# Create a new folder
@api_routes.route('/folder', methods=['POST'])
def create_folder():
    data = request.json
    new_folder = File(name=data['name'], folder_size=data['folder_size'])

    db.session.add(new_folder)
    db.session.commit()

    return jsonify({'folder': {'id': new_folder.id, 'name': new_folder.name, 'folder_size': new_folder.folder_size}})


# Update an existing folder
@api_routes.route('/folder/<int:folder_id>', methods=['PUT'])
def update_folder(folder_id):
    data = request.json
    folder = folder.query.get(folder_id)
    if not folder:
        return jsonify({'error': 'Folder not found'})

    data = request.json
    folder.name = data.get('name', folder.name)
    folder.folder_size = data.get('folder_size', folder.folder_size)

    db.session.commit()
    return jsonify({'file': {'id': folder.id, 'name': folder.name, 'folderize': folder.folder_size, 'folder_type': folder.folder_type, 'folder_path': folder.folder_path}})

# Delete a folder


@api_routes.route('/folder/<folder_id>', methods=['DELETE'])
def delete_folder(folder_id):
    folder = folder.query.get(folder_id)
    if not folder:
        return jsonify({'error: folder not found'})

    db.session.delete(folder)
    db.session.commit()

    return jsonify({'result': True})


# restore_path


@api_routes.route('/users', methods=['GET'])
def get_user():
    users = User.query.all()
    # print(users[0])
    # "password": '',
    # "isFirstTime": True,
    return jsonify({'user': [{'name': user.name, "backup_schedule": user.backup_schedule, "backedup_at": user.backedup_at, "restore_path": user.restore_path, "password": user.password, "isFirstTime": user.isFirstTime, "total_data": user.total_data}for user in users]})


# @api_routes.route('/user', methods=['POST'])
# def new_user():
#     data = request.json
#     user = User(name=data['name'], password=data["password"], isFirstTime=data["isFirstTime"], backup_schedule=data['backup_schedule'],
#                 total_data=data['total_data'])

#     db.session.add(user)
#     db.session.commit()
#     print(user)
#     return jsonify({'user': {'name': user.name, "backup_schedule": user.backup_schedule, "backedup_at": user.backedup_at, "user": user.restore_path, "total_data": user.total_data, "isFirstTime": user.isFirstTime, "password": user.password}})


@api_routes.route('/user', methods=["POST"])
def create_user():
    data = request.json
    user = User(name=data["name"], password=data["password"],
                isFirstTime=data["isFirstTime"])

    db.session.add(user)
    db.session.commit()
    return ({"user": {"name": user.name, "password": user.password, "isFirstTime": user.isFirstTime, "backup_schedule": user.backup_schedule, "total_data": user.total_data, "restore_path": user.restore_path}})
    # id = db.Column(db.Integer, primary_key=True)
    # name = db.Column(db.String(100), nullable=False)
    # password = db.Column(db.String, nullable=False)
    # isFirstTime = db.Column(db.Boolean, default=True)
    # backup_schedule = db.Column(db.String)
    # backedup_at = db.Column(DateTime, default=None)
    # total_data = db.Column(db.String)
    # restore_path = db.Column(db.String)
# @api_routes.route('/folder', methods=['POST'])
# def create_folder():
#     data = request.json
#     new_folder = File(name=data['name'], folder_size=data['folder_size'])

#     db.session.add(new_folder)
#     db.session.commit()

#     return jsonify({'folder': {'id': new_folder.id, 'name': new_folder.name, 'folder_size': new_folder.folder_size}})


@api_routes.route('/updateUser', methods=['PUT'])
def update_user():
    data = request.json
    with open("C:\\Users\\Donkor James\\Auto_backup2\\Auto_backup\\userData.json", "r") as file:
        login_credentials = json.load(file)

        user = User.query.get(login_credentials["id"])
        print(data, "this is update data line 185")
        print(user, "This is the user to be updated 186")

        user.name = data.get("name", user.name)
        # user.password = data.get("password", user.password)
        user.isFirstTime = data.get("isFirstTime", user.isFirstTime)
        user.backup_schedule = data.get(
            "backup_schedule", user.backup_schedule)
        user.restore_path = data.get("restore_path", user.restore_path)
        user.total_data = data.get("total_data", user.total_data)

        db.session.commit()
        print(user, "this is user after updated")

        return jsonify({'user': {'name': user.name, "backup_schedule": user.backup_schedule, "restore_path": user.restore_path, "total_data": user.total_data, "password": user.password}})


@api_routes.route('/getUser', methods=['GET'])
def user():
    with open(file_path, "r") as file:
        login_credentials = json.load(file)
        print(login_credentials, "login_cred")

        user = User.query.get(login_credentials["id"])
        print(user, "this getUser in the settings page line 209")
        return jsonify({'user': {'name': user.name, "backup_schedule": user.backup_schedule, "restore_path": user.restore_path, "total_data": user.total_data, "password": user.password, "isFirstTime": user.isFirstTime}})


@api_routes.route('/login', methods=['POST'])
def login():
    data = request.json
    # print(data)
    username = data["name"]
    password = data['password']
    user = User.query.filter_by(name=username).first()
    # print(user, userId)
    # print(user.password, password)
    if user and user.password == password:
        login_credentials = {"isValid": True,
                             "isFirstTime": user.isFirstTime, "id": user.id}
        print(login_credentials, "line 225 and ", user)

        with open(file_path, "w") as file:
            json.dump(login_credentials, file)

        return jsonify({"valid": login_credentials})
    else:
        print("naaa")
        return jsonify({"valid": {"isValid": False}})
