from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), nullable=False)


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
        return f"folder('{self.name}', '{self.folder_size}!')"

# with app
# db.create_all()
