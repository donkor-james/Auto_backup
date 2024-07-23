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
    db.drop_all()
    db.metadata.clear()

# with app.app_context():
#     # db.drop_all()
#     db.create_all()

# # Run Server
if __name__ == '__main__':
    app.run(debug=True)
