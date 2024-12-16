from . import conversion
import os
import logging
from flask import Blueprint, request, jsonify, send_file, current_app
from werkzeug.utils import secure_filename
import mimetypes
import ffmpeg

ALLOWED_EXTENSIONS = {'mp3', 'wav', 'flac', 'aac', 'ogg'}
MAX_FILE_SIZE = 10 * 1024 * 1024  # Limit file size to 10 MB (adjust as needed)

def allowed_file(filename):
    """Check if the file has an allowed extension."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def check_audio_file(file_path):
    """Check if the uploaded file is a valid audio file using ffmpeg."""
    try:
        # Run ffmpeg probe to check if the file is a valid audio file
        probe = ffmpeg.probe(file_path, v='error', select_streams='a', show_entries='stream=codec_type')
        # If there is an audio stream in the file, it's a valid audio file
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
    target_format = request.form.get('target_format', 'mp3').lower()  # Default to MP3 if not provided

    # Check if the file extension is allowed
    if not allowed_file(file.filename):
        return jsonify({"error": "Invalid file format. Supported formats are MP3, WAV, FLAC, AAC, OGG."}), 400

    # Check MIME type (this adds a second layer of validation)
    mime_type, _ = mimetypes.guess_type(file.filename)
    if not mime_type or not mime_type.startswith("audio/"):
        return jsonify({"error": "Invalid MIME type. Only audio files are allowed."}), 400

    # Check if the file size exceeds the limit
    if len(file.read()) > MAX_FILE_SIZE:
        return jsonify({"error": f"File is too large. Maximum size is {MAX_FILE_SIZE / (1024 * 1024)} MB."}), 400
    file.seek(0)  # Reset file pointer after checking size

    # Save the uploaded file to a temporary location
    uploaded_filename = os.path.join(current_app.config['UPLOAD_FOLDER'], secure_filename(file.filename))
    file.save(uploaded_filename)

    # Check if the uploaded file is a valid audio file using FFmpeg
    if not check_audio_file(uploaded_filename):
        os.remove(uploaded_filename)  # Cleanup if invalid audio
        return jsonify({"error": "The uploaded file is not a valid audio file."}), 400

    try:
        # Determine output filename and path based on target format
        output_filename = os.path.splitext(file.filename)[0] + f'.{target_format}'
        output_filepath = os.path.join(current_app.config['CONVERT_FOLDER'], output_filename)

        # Log file paths for debugging
        logging.debug(f"Uploaded file saved to: {uploaded_filename}")
        logging.debug(f"Converted file will be saved to: {output_filepath}")

        # Convert the audio file using FFmpeg
        ffmpeg.input(uploaded_filename).output(output_filepath).run()

        # Ensure the converted file exists
        if not os.path.exists(output_filepath):
            return jsonify({"error": "File conversion failed: output file not found"}), 500

    except Exception as e:
        logging.error(f"Error during conversion: {e}")
        return jsonify({"error": f"Error converting audio: {e}"}), 500

    finally:
        # Cleanup: Remove the uploaded file after conversion
        if os.path.exists(uploaded_filename):
            os.remove(uploaded_filename)

    # Return a download link pointing to the converted file
    return jsonify({"success": True, "download_link": f"/download/{output_filename}"})



@conversion.route('/download/<filename>', methods=['GET'])
def download(filename):
    # Fetch the file from CONVERT_FOLDER
    filepath = os.path.join(current_app.config['CONVERT_FOLDER'], filename)
    if not os.path.exists(filepath):
        return jsonify({"error": "File not found"}), 404

    try:
        # Send the file as a response
        response = send_file(filepath, as_attachment=True)

        # Schedule file removal after the response is closed
        response.call_on_close(lambda: os.remove(filepath) if os.path.exists(filepath) else None)

        logging.debug(f"File sent for download and scheduled for deletion: {filepath}")
        return response
    except Exception as e:
        logging.error(f"Error sending file: {e}")
        return jsonify({"error": f"Error sending file: {e}"}), 500
