from flask import Flask, request, jsonify, current_app
from werkzeug.utils import secure_filename
from . import bpm
import essentia
import essentia.standard as es
import os


ALLOWED_EXTENSIONS = {'wav', 'mp3', 'flac'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@bpm.route('/analyze', methods=['POST', 'GET'])
def analyze():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files['file']

    if file.filename == '' or not allowed_file(file.filename):
        return jsonify({"error": "Invalid file type"}), 400

    filename = secure_filename(file.filename)
    file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)  # Accessing upload folder from config
    file.save(file_path)

    try:
        # Perform BPM and key analysis here...
        audio = es.MonoLoader(filename=file_path)()
        rhythm_extractor = es.RhythmExtractor2013(method="multifeature")
        bpm, beats, beats_confidence, _, beats_intervals = rhythm_extractor(audio)
        rounded_bpm = round(bpm)
        key_extractor = es.KeyExtractor()
        key, scale, strength = key_extractor(audio)

        result_data = {
            "BPM": rounded_bpm,
            "Key": key
        }

    finally:
        # Cleanup: Remove the uploaded file after processing
        if os.path.exists(file_path):
            os.remove(file_path)

    return jsonify(result_data)

