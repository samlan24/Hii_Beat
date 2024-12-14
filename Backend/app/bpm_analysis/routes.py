from flask import request, jsonify, current_app, session
from werkzeug.utils import secure_filename
from . import bpm
import essentia.standard as es
from datetime import datetime, timedelta
import os

ALLOWED_EXTENSIONS = {'wav', 'mp3', 'flac'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@bpm.route('/analyze', methods=['POST'])
def analyze():
    db = current_app.config['db']
    uploads_collection = db.uploads
    now = datetime.utcnow()

    # Check if the session ID exists; if not, create one (handled by Flask-Session)
    session_id = session.get('session_id')
    if not session_id:
        session_id = os.urandom(16).hex()  # Generate a new session ID
        session['session_id'] = session_id  # Save the session ID in the session

    one_day_ago = now - timedelta(days=1)

    # Query the user's uploads in the last 24 hours
    recent_uploads = list(uploads_collection.find({
        "session_id": session_id,
        "timestamp": {"$gte": one_day_ago}
    }))

    # Check if user has exceeded the daily limit
    if len(recent_uploads) >= 5:
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
        result_data = {
            "BPM": rounded_bpm,
            "Key": key
        }
        # Add the current upload to MongoDB
        uploads_collection.insert_one({
            "session_id": session_id,
            "timestamp": now,
            "filename": filename
        })
    finally:
        # Cleanup the uploaded file
        if os.path.exists(file_path):
            os.remove(file_path)

    return jsonify(result_data)