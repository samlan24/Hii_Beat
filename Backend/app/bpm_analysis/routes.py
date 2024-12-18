from flask import request, jsonify, current_app, session
from werkzeug.utils import secure_filename
from . import bpm
import essentia.standard as es
from datetime import datetime
import os
from app.utils.sessions_utils import check_daily_limit  # Import the helper function

ALLOWED_EXTENSIONS = {'wav', 'mp3', 'flac'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Mapping of musical keys to Camelot notation
KEY_TO_CAMELOT = {
    'C': '8B', 'C#': '3B', 'D': '10B', 'D#': '5B', 'E': '12B', 'F': '7B', 'F#': '2B', 'G': '9B', 'G#': '4B', 'A': '11B', 'A#': '6B', 'B': '1B',
    'Cm': '5A', 'C#m': '12A', 'Dm': '7A', 'D#m': '2A', 'Em': '9A', 'Fm': '4A', 'F#m': '11A', 'Gm': '6A', 'G#m': '1A', 'Am': '8A', 'A#m': '3A', 'Bm': '10A'
}

@bpm.route('/analyze', methods=['POST'])
def analyze():
    db = current_app.config['db']
    uploads_collection = db.uploads

    # Check if user has exceeded the daily upload limit
    if not check_daily_limit():  # Use the helper function
        return jsonify({"error": "Daily upload limit reached. Try again tomorrow."}), 403

    # Process the uploaded file
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files['file']

    if file.filename == '' or not allowed_file(file.filename):
        return jsonify({"error": "Invalid file type"}), 400

    filename = secure_filename(file.filename)
    file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)

    file.save(file_path)

    try:
        # Perform BPM and key analysis
        audio = es.MonoLoader(filename=file_path)()
        rhythm_extractor = es.RhythmExtractor2013(method="multifeature")
        bpm_value, beats, beats_confidence, _, beats_intervals = rhythm_extractor(audio)
        rounded_bpm = round(bpm_value)
        key_extractor = es.KeyExtractor()
        key, scale, strength = key_extractor(audio)

        # Determine Camelot notation
        camelot_key = KEY_TO_CAMELOT.get(f"{key}{'m' if scale == 'minor' else ''}", "Unknown")

        result_data = {
            "BPM": rounded_bpm,
            "Key": key,
            "Camelot": camelot_key
        }

        # Add the current upload to MongoDB
        session_id = session.get('session_id')  # Get session ID from session
        uploads_collection.insert_one({
            "session_id": session_id,
            "timestamp": datetime.utcnow(),
            "filename": filename
        })

    finally:
        # Cleanup the uploaded file
        if os.path.exists(file_path):
            os.remove(file_path)

    return jsonify(result_data)