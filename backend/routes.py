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


# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///example.db'
# db = SQLAlchemy(app)


# # class User(db.Model):
# #     id = db.Column(db.Integer, primary_key=True)
# #     username = db.Column(db.String(50), unique=True)
# #     email = db.Column(db.String(50), unique=True)


# # class UserSchema(Schema):
# #     id = fields.Int(dump_only=True)
# #     username = fields.Str(required=True)
# #     email = fields.Email(required=True)


# # @app.route('/users', methods=['GET'])
# # def get_users():
# #     users = User.query.all()
# #     user_schema = UserSchema(many=True)
# #     result = user_schema.dump(users)
# #     return jsonify(result)


# # @app.route('/users', methods=['POST'])
# # def create_user():
# #     user_schema = UserSchema()
# #     new_user = user_schema.load(request.json)
# #     db.session.add(new_user)
# #     db.session.commit()
# #     return user_schema.jsonify(new_user)


# # if __name__ == '__main__':
# #     db.create_all()
# #     app.run(debug=True)

# # class Folder(db.Model):
# #     id = db.Column(db.Integer, primary_key=True)
# #     name = db.Column()
# #     size = db.Column()
# # Start


# from flask import Flask, request, jsonify
# from flask_sqlalchemy import SQLAlchemy
# from flask_marshmallow import Marshmallow
# import os

# app = Flask(__name__)
# # app = app.createp

# basedir = os.path.abspath(os.path.dirname(__folder__))
# basedir = basedir.replace('api', '')
# print(basedir)
# # Database
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
#     os.path.join(basedir, 'db.sqlite')
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# #
# db = SQLAlchemy(app)
# # with app.app_context():
# #     db.create_all()
# # Init ma
# ma = Marshmallow(app)


# class File(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(100))
#     size = db.Column(db.Integer)
#     file_type = db.Column(db.String(100))
#     file_path = db.Column(db.String(100))

#     def __init__(self, name, size, file_type, file_path):
#         self.name = name
#         self.size = size
#         self.file_type = file_type
#         self.file_path = file_path

# # file schema


# class folderchema(ma.Schema):
#     class Meta:
#         model = File
#         fields = ('id', 'name', 'size', 'file_type', 'file_path')


# # Init schema
# file_schema = FileSchema(unknown='raise')
# files_schema = FileSchema(many=True, unknown='raise')

# # Create a file


# @app.route('/file', methods=['POST'])
# def add_file():
#     name = request.json['name']
#     size = request.json['size']
#     file_type = request.json['file_type']
#     file_path = request.json['file_path']

#     new_file = File(name=name, size=size, file_type=file_type, file_path)

#     db.session.add(new_file)
#     db.session.commit()

#     return file_schema.jsonify(new_file)

# # Get all files


# @app.route('/file', methods=['GET'])
# def get_files():
#     all_files = File.query.all()
#     result = files_schema.dump(all_files)
#     return jsonify(result.data)


# # Run Server
# if __name__ == '__main__':
#     app.run(debug=True)

# file = "file.txt"
# if '.' in file:
#     f_type = file.split('.')[-1]
# else:
#     f_type = None

# print(f_type)
