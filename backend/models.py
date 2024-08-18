from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import DateTime
from datetime import datetime

db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String, nullable=False)
    isFirstTime = db.Column(db.Boolean, default=True)
    backup_schedule = db.Column(db.String)
    backedup_at = db.Column(DateTime, default=None)
    total_data = db.Column(db.String)
    restore_path = db.Column(db.String)

    def __repr__(self):
        return f"User('{self.name}', '{self.password}', {self.isFirstTime}, '{self.id}, {self.restore_path}, {self.backup_schedule}')"


class File(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    file_size = db.Column(db.String, nullable=False)
    file_type = db.Column(db.String)
    file_path = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f"File('{self.name}', '{self.file_size}', {self.file_type}, '{self.file_path}')"


class Folder(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    folder_size = db.Column(db.String)

    def __repr__(self):
        return f"folder('{self.name}', '{self.folder_size}, {self.id}')"


#     print("yess")
# if "User" in db.metadata.tables:
#     print("yess!")
#     db.metadata.tables["User"].drop(db.engine)
# with app.a:
#     db.create_all()
