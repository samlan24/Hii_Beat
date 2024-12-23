from flask import Flask
from flask_cors import CORS
from flask_session import Session  # Import Flask-Session
from pymongo import MongoClient
import os
from datetime import timedelta

mongo_client = None

def create_app():
    app = Flask(__name__)
    CORS(app, supports_credentials=True)

    app.secret_key = "hello"

    # Configure Flask-Session
    app.config['SESSION_TYPE'] = 'mongodb'  # Use MongoDB for session storage
    app.config['SESSION_MONGODB'] = mongo_client  # Your MongoDB client instance
    app.config['SESSION_PERMANENT'] = True  # Set to True if you want persistent sessions
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=1)

    # Initialize the session extension
    Session(app)

    # Connect to MongoDB
    MONGO_URI = "mongodb://localhost:27017/project"
    client = MongoClient(MONGO_URI)
    app.config['db'] = client.get_database('project')

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
