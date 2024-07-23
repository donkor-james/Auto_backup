import os
from flask import request, jsonify, Blueprint
from models import db, File, Folder, User

api_routes = Blueprint('api', __name__)


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


backup_schedule = db.column(db.String)
# restore_path


@api_routes.route('/user', methods=['GET'])
def get_user():
    user = User.query.get(1)
    return jsonify({'user': {'id': user.id, 'name': user.name, "backup_schedule": user.backup_schedule, "backedup_at": user.backedup_at, "total_data": user.total_data}})

    # name = db.Column(db.String(100), nullable=False)
    # backup_schedule = db.column(db.String)
    # backedup_at = db.column(DateTime, default=None)
    # total_data = db.Column(db.String)


@api_routes.route('/user/<int:id>', methods=['POST'])
def update_user(id):
    data = request.json
    user = User.query.get(id)
    user.name = data.get("name", user.name)
    user.backup_schedule = data.get("name", user.backup_schedule)
    user.backedup_at = data.get("name", user.backedup_at)
    user.total_data = data.get("name", user.total_data)
    db.session.commit()

    return jsonify({'user': {'id': user.id, 'email': user.email}})


@api_routes.route('/test', methods=['POST'])
def update_test(id):
    # data = request.json
    # user = User.query.get(id)
    # user.email = data.get("email", user.email)
    # db.session.commit()

    return jsonify({'test': {'id': "test_id", 'email': "test_email"}})
