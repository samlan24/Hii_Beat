from flask import Flask
from flask_cors import CORS
from flask_session import Session
from pymongo import MongoClient
from datetime import timedelta
import os

def create_app():
    app = Flask(__name__)
    CORS(app, supports_credentials=True)

    app.secret_key = "hello"  # Secret key for session management

    # MongoDB Configuration for Flask-Session
    MONGO_URI = "mongodb://localhost:27017/music"  # MongoDB URI
    mongo_client = MongoClient(MONGO_URI)  # Create a MongoClient instance

    # Configure Flask-Session to use MongoDB
    app.config['SESSION_TYPE'] = 'mongodb'  # Flask-Session type
    app.config['SESSION_MONGODB'] = mongo_client  # Pass the MongoDB client instance
    app.config['SESSION_PERMANENT'] = True  # Whether the session is permanent
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=1)  # Session lifetime (1 day)

    # Initialize the session extension
    Session(app)  # Initializes Flask-Session with the app

    # Set up MongoDB database
    app.config['db'] = mongo_client.get_database('music')

    # Define the upload folder paths
    UPLOAD_FOLDER = os.path.join(app.root_path, 'static', 'uploads')
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    CONVERT_FOLDER = os.path.join(app.root_path, 'static', 'converted')
    app.config['CONVERT_FOLDER'] = CONVERT_FOLDER

    # Ensure the upload folder exists
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)

    if not os.path.exists(CONVERT_FOLDER):
        os.makedirs(CONVERT_FOLDER)

    # Register blueprints
    from .auth import auth
    app.register_blueprint(auth)

    from .bpm_analysis import bpm
    app.register_blueprint(bpm)

    from .bpm_change import bpm_change
    app.register_blueprint(bpm_change)

    from .conversion import conversion
    app.register_blueprint(conversion)

    return app
