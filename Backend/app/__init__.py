from flask import Flask
from flask_cors import CORS
from pymongo import MongoClient
import os


mongo_client = None

def create_app():
    app = Flask(__name__)
    CORS(app)

    app.secret_key = "hello"

    # Connect to MongoDB
    MONGO_URI = "mongodb://localhost:27017/music"
    client = MongoClient(MONGO_URI)
    app.config['db'] = client.get_database('music')

    # Define the upload folder path
    UPLOAD_FOLDER = os.path.join(app.root_path, 'static', 'uploads')
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    CONVERT_FOLDER = os.path.join(app.root_path, 'static', 'converted')
    app.config['CONVERT_FOLDER'] = CONVERT_FOLDER

    # Ensure the upload folder exists
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)

    if not os.path.exists(CONVERT_FOLDER):
        os.makedirs(CONVERT_FOLDER)

    from .auth import auth
    app.register_blueprint(auth)

    from .bpm_analysis import bpm
    app.register_blueprint(bpm)

    from .bpm_change import bpm_change
    app.register_blueprint(bpm_change)

    from .conversion import conversion
    app.register_blueprint(conversion)

    return app