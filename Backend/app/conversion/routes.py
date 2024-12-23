from . import conversion
import os
import logging
from flask import Blueprint, request, jsonify, send_file, current_app
from werkzeug.utils import secure_filename
import mimetypes
import ffmpeg

ALLOWED_EXTENSIONS = {'mp3', 'wav', 'flac', 'aac', 'ogg'}
MAX_FILE_SIZE = 10 * 1024 * 1024

def allowed_file(filename):
    """Check if the file has an allowed extension."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def check_audio_file(file_path):
    """Check if the uploaded file is a valid audio file using ffmpeg."""
    try:

        probe = ffmpeg.probe(file_path, v='error', select_streams='a', show_entries='stream=codec_type')

        if 'streams' in probe and len(probe['streams']) > 0 and probe['streams'][0]['codec_type'] == 'audio':
            return True
    except ffmpeg.Error as e:
        logging.error(f"FFmpeg error: {e}")
    return False

@conversion.route('/convert', methods=['POST'])
def convert_audio():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files['file']
    target_format = request.form.get('target_format', 'mp3').lower()


    if not allowed_file(file.filename):
        return jsonify({"error": "Invalid file format. Supported formats are MP3, WAV, FLAC, AAC, OGG."}), 400


    mime_type, _ = mimetypes.guess_type(file.filename)
    if not mime_type or not mime_type.startswith("audio/"):
        return jsonify({"error": "Invalid MIME type. Only audio files are allowed."}), 400


    if len(file.read()) > MAX_FILE_SIZE:
        return jsonify({"error": f"File is too large. Maximum size is {MAX_FILE_SIZE / (1024 * 1024)} MB."}), 400
    file.seek(0)


    uploaded_filename = os.path.join(current_app.config['UPLOAD_FOLDER'], secure_filename(file.filename))
    file.save(uploaded_filename)


    if not check_audio_file(uploaded_filename):
        os.remove(uploaded_filename)
        return jsonify({"error": "The uploaded file is not a valid audio file."}), 400

    try:

        output_filename = os.path.splitext(file.filename)[0] + f'.{target_format}'
        output_filepath = os.path.join(current_app.config['CONVERT_FOLDER'], output_filename)


        logging.debug(f"Uploaded file saved to: {uploaded_filename}")
        logging.debug(f"Converted file will be saved to: {output_filepath}")


        ffmpeg.input(uploaded_filename).output(output_filepath).run()


        if not os.path.exists(output_filepath):
            return jsonify({"error": "File conversion failed: output file not found"}), 500

    except Exception as e:
        logging.error(f"Error during conversion: {e}")
        return jsonify({"error": f"Error converting audio: {e}"}), 500

    finally:

        if os.path.exists(uploaded_filename):
            os.remove(uploaded_filename)


    return jsonify({"success": True, "download_link": f"/download/{output_filename}"})



@conversion.route('/download/<filename>', methods=['GET'])
def download(filename):

    filepath = os.path.join(current_app.config['CONVERT_FOLDER'], filename)
    if not os.path.exists(filepath):
        return jsonify({"error": "File not found"}), 404

    try:

        response = send_file(filepath, as_attachment=True)


        response.call_on_close(lambda: os.remove(filepath) if os.path.exists(filepath) else None)

        logging.debug(f"File sent for download and scheduled for deletion: {filepath}")
        return response
    except Exception as e:
        logging.error(f"Error sending file: {e}")
        return jsonify({"error": f"Error sending file: {e}"}), 500
