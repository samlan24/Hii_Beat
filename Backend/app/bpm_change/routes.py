from flask import Blueprint, request, jsonify, send_file, current_app, session, after_this_request
import librosa
import soundfile as sf
import os
from datetime import datetime
from app.utils.sessions_utils import check_daily_limit  # Import the helper function

from . import bpm_change

@bpm_change.route('/transpose', methods=['POST'])
def transpose():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files['file']

    # Check if the uploaded file is an audio file (MP3 or WAV)
    if not (file.filename.endswith('.mp3') or file.filename.endswith('.wav')):
        return jsonify({"error": "Invalid file type. Only MP3 and WAV files are allowed."}), 400

    # Check if user has exceeded the daily upload limit
    if not check_daily_limit():  # Use the helper function
        return jsonify({"error": "Daily upload limit reached. Try again tomorrow."}), 403

    transpose_steps = int(request.form.get('transpose_steps', 0))  # Default to no transposition

    # Save uploaded audio file temporarily
    uploaded_filename = os.path.join(current_app.config['UPLOAD_FOLDER'], file.filename)
    file.save(uploaded_filename)

    transposed_filepath = None  # Initialize to avoid UnboundLocalError

    try:
        # Process the file with Librosa
        y, sr = librosa.load(uploaded_filename, sr=None)
        y_transposed = librosa.effects.pitch_shift(y, sr=sr, n_steps=transpose_steps)

        # Save the transposed file in the CONVERT_FOLDER
        transposed_filename = f"transposed_{file.filename}"
        transposed_filepath = os.path.join(current_app.config['CONVERT_FOLDER'], transposed_filename)
        sf.write(transposed_filepath, y_transposed, sr)

        # Add the current upload to MongoDB
        uploads_collection = current_app.config['db'].uploads
        uploads_collection.insert_one({
            "session_id": session['session_id'],
            "timestamp": datetime.utcnow(),
            "filename": file.filename
        })

        # Return the download link
        download_link = f"/download/{transposed_filename}"
        return jsonify({"success": True, "download_link": download_link})

    finally:
        # Cleanup the uploaded file
        if os.path.exists(uploaded_filename):
            os.remove(uploaded_filename)

@bpm_change.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    file_path = os.path.join(current_app.config['CONVERT_FOLDER'], filename)
    if os.path.exists(file_path):
        @after_this_request
        def remove_file(response):
            try:
                os.remove(file_path)
            except Exception as error:
                current_app.logger.error(f"Error removing file: {error}")
            return response
        return send_file(file_path, as_attachment=True)
    else:
        return jsonify({"error": "File not found"}), 404