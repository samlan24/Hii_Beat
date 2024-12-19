from flask import Flask
from flask_cors import CORS
from flask_session import Session
from pymongo import MongoClient
import os
from datetime import timedelta
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def create_app():
    app = Flask(__name__)
    CORS(app, supports_credentials=True)

    app.secret_key = os.environ.get('FLASK_SECRET_KEY')

    # Configure Flask-Session
    app.config['SESSION_TYPE'] = 'mongodb'
    app.config['SESSION_MONGODB'] = MongoClient(os.environ.get('MONGO_URI'))
    app.config['SESSION_PERMANENT'] = True
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=1)

    # Initialize the session extension
    Session(app)

    # Connect to MongoDB
    mongo_client = MongoClient(os.environ.get('MONGO_URI'))
    app.config['db'] = mongo_client.get_database('music')





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