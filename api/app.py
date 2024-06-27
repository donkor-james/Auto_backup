from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema, fields
import os

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
basedir = basedir.replace('api', '')

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
    os.path.join(basedir, 'db.sqlite')

db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), nullable=False)


class File(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    file_size = db.Column(db.Integer, nullable=False)
    file_type = db.Column(db.String, nullable=False)
    file_path = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f"File('{self.name}', '{self.file_size}', {self.file_type}, '{self.file_path}')"

# Get all files


@app.route('/api/files', methods=['GET'])
def get_file():
    files = File.query.all()
    return jsonify({'files': [{'id': file.id, 'name': file.name, 'file_size': file.file_size, 'file_type': file.file_type, 'file_path': file.file_path} for file in files]})


# Create a new file
@app.route('/api/file', methods=['POST'])
def create_file():
    data = request.json
    new_file = File(name=data['name'], file_size=data['file_size'],
                    file_type=data['file_type'], file_path=data['file_path'])

    db.session.add(new_file)
    db.session.commit()

    return jsonify({'file': {'id': new_file.id, 'name': new_file.name, 'filesize': new_file.file_size, 'file_type': new_file.file_type, 'filepath': new_file.file_path}})


# Update an existing file
@app.route('/api/files/<int:file_id>', methods=['PUT'])
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


@app.route('/api/files/<file_id>', methods=['DELETE'])
def delete_file(file_id):
    file = File.query.get(file_id)
    if not file:
        return jsonify({'error: File not found'})

    db.session.delete(file)
    db.session.commit()

    return jsonify({'result': True})


# # Run Server
if __name__ == '__main__':
    app.run(debug=True)


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

# basedir = os.path.abspath(os.path.dirname(__file__))
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


# class FileSchema(ma.Schema):
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
