from flask import Blueprint, request, jsonify, send_file, current_app, session, after_this_request
import librosa
import soundfile as sf
import os
from datetime import datetime
from werkzeug.utils import secure_filename
import mimetypes
from app.utils.sessions_utils import check_daily_limit

from . import bpm_change

"""route to change the pitch of an uploaded audio file"""

ALLOWED_EXTENSIONS = {'mp3', 'wav'}
MAX_FILE_SIZE = 10 * 1024 * 1024

def allowed_file(filename):
    """Check if the file has an allowed extension (MP3 or WAV)."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def is_valid_audio(file_path):
    """Ensure the uploaded file is a valid audio file using Librosa."""
    try:
        y, sr = librosa.load(file_path, sr=None)  # Load the file to check if it's a valid audio
        return True
    except Exception as e:
        current_app.logger.error(f"Invalid audio file: {e}")
        return False

@bpm_change.route('/transpose', methods=['POST'])
def transpose():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files['file']


    if not allowed_file(file.filename):
        """check file extension"""
        return jsonify({"error": "Invalid file type. Only MP3 and WAV files are allowed."}), 400


    mime_type, _ = mimetypes.guess_type(file.filename)
    if not mime_type or not mime_type.startswith('audio/'):
        """check MIME type"""
        return jsonify({"error": "Invalid MIME type. Only audio files are allowed."}), 400


    if not check_daily_limit():
        """check daily limit"""
        return jsonify({"error": "Daily upload limit reached. Try again tomorrow."}), 403


    if len(file.read()) > MAX_FILE_SIZE:
        """check file size"""
        return jsonify({"error": f"File size exceeds the {MAX_FILE_SIZE / (1024 * 1024)} MB limit."}), 400
    file.seek(0)

    # Save uploaded audio file temporarily
    uploaded_filename = os.path.join(current_app.config['UPLOAD_FOLDER'], secure_filename(file.filename))
    file.save(uploaded_filename)

    if not is_valid_audio(uploaded_filename):
        os.remove(uploaded_filename)
        return jsonify({"error": "The uploaded file is not a valid audio file."}), 400

    transpose_steps = int(request.form.get('transpose_steps', 0))

    transposed_filepath = None  # Initialize to avoid UnboundLocalError

    try:

        y, sr = librosa.load(uploaded_filename, sr=None)
        y_transposed = librosa.effects.pitch_shift(y, sr=sr, n_steps=transpose_steps)


        transposed_filename = f"transposed_{file.filename}"
        transposed_filepath = os.path.join(current_app.config['CONVERT_FOLDER'], transposed_filename)
        sf.write(transposed_filepath, y_transposed, sr)


        uploads_collection = current_app.config['db'].uploads
        uploads_collection.insert_one({
            "session_id": session['session_id'],
            "timestamp": datetime.utcnow(),
            "filename": file.filename
        })


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
