from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema, fields
import os
from flask_cors import CORS
from routes import api_routes
from models import db

app = Flask(__name__)
CORS(app)
app.register_blueprint(api_routes, url_prefix='/api')

basedir = os.path.abspath(os.path.dirname(__file__))
basedir = basedir.replace('api', '')
basedir = basedir.replace('backend', '')

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
    os.path.join(basedir, 'db.sqlite')

path = os.path.join(basedir, 'db.sqlite')
db.init_app(app)

with app.app_context():
    db.create_all()

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

# file = "file.txt"
# if '.' in file:
#     f_type = file.split('.')[-1]
# else:
#     f_type = None

# print(f_type)
