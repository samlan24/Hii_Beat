import os
import logging
from flask import Blueprint, request, jsonify, send_file, current_app
from pydub import AudioSegment
from . import conversion

@conversion.route('/convert', methods=['POST'])
def convert_mp3_to_wav():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files['file']

    # Save uploaded MP3 file temporarily in UPLOAD_FOLDER
    uploaded_filename = os.path.join(current_app.config['UPLOAD_FOLDER'], file.filename)
    file.save(uploaded_filename)

    try:
        # Generate the output file path in CONVERT_FOLDER
        wav_filename = os.path.splitext(file.filename)[0] + '.wav'
        wav_filepath = os.path.join(current_app.config['CONVERT_FOLDER'], wav_filename)

        # Log file paths for debugging
        logging.debug(f"Uploaded file saved to: {uploaded_filename}")
        logging.debug(f"Converted file will be saved to: {wav_filepath}")

        # Load MP3 and export as WAV
        audio = AudioSegment.from_mp3(uploaded_filename)
        audio.export(wav_filepath, format='wav')

        # Ensure the converted file exists
        if not os.path.exists(wav_filepath):
            return jsonify({"error": "File conversion failed: output file not found"}), 500

    except Exception as e:
        logging.error(f"Error during conversion: {e}")
        return jsonify({"error": f"Error converting audio: {e}"}), 500

    finally:
        # Cleanup: Remove the uploaded MP3 file after conversion
        if os.path.exists(uploaded_filename):
            os.remove(uploaded_filename)

    # Return a download link pointing to the converted file
    return jsonify({"success": True, "download_link": f"/download/{wav_filename}"})


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
