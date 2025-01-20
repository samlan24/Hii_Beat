from flask import request, jsonify, current_app, session
from werkzeug.utils import secure_filename
from . import bpm
import essentia.standard as es
from datetime import datetime
import os

""" route to analyze the BPM and key of an uploaded audio file """

ALLOWED_EXTENSIONS = {'wav', 'mp3', 'flac'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@bpm.route('/analyze', methods=['POST'])
def analyze():

    from app.utils.sessions_utils import check_daily_limit

    db = current_app.config['db']
    uploads_collection = db.uploads


    if not check_daily_limit():
        return jsonify({"error": "Daily upload limit reached. Try again tomorrow."}), 403


    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files['file']

    if file.filename == '' or not allowed_file(file.filename):
        return jsonify({"error": "Invalid file type"}), 400

    filename = secure_filename(file.filename)
    file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)

    file.save(file_path)

    try:

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

        """Add the current upload to MongoDB"""
        session_id = session.get('session_id')
        uploads_collection.insert_one({
            "session_id": session_id,
            "timestamp": datetime.utcnow(),
            "filename": filename
        })

    finally:
        """Cleanup the uploaded file"""
        if os.path.exists(file_path):
            os.remove(file_path)

    return jsonify(result_data)
