from . import spleeter
import os
import logging
from flask import Flask, request, jsonify, send_file, current_app
from spleeter.separator import Separator

@spleeter.route('/spleet', methods=['POST', 'GET'])
def separate_audio():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files['file']

    # Save uploaded file
    input_path = os.path.join(current_app.config['UPLOAD_FOLDER'], file.filename)
    file.save(input_path)

    try:
        # Initialize Spleeter (2 stems: vocals and accompaniment)
        separator = Separator('spleeter:2stems')

        # Set output directory
        output_dir = os.path.join(current_app.config['CONVERT_FOLDER'], os.path.splitext(file.filename)[0])
        os.makedirs(output_dir, exist_ok=True)

        # Perform separation
        separator.separate_to_file(input_path, output_dir)

        # Retrieve paths for separated files
        vocal_path = os.path.join(output_dir, 'vocals.wav')
        accompaniment_path = os.path.join(output_dir, 'accompaniment.wav')

        if not os.path.exists(vocal_path) or not os.path.exists(accompaniment_path):
            return jsonify({"error": "Separation failed"}), 500

        # Optionally, clean up the input file
        os.remove(input_path)

        return jsonify({
            "success": True,
            "vocal_download_link": f"/spleeter/download/{os.path.basename(vocal_path)}",
            "accompaniment_download_link": f"/spleeter/download/{os.path.basename(accompaniment_path)}"
        })

    except Exception as e:
        logging.error(f"Error during separation: {e}")
        return jsonify({"error": f"Error during separation: {e}"}), 500


@spleeter.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    # Path to output file
    filepath = os.path.join(current_app.config['CONVERT_FOLDER'], filename)
    if not os.path.exists(filepath):
        return jsonify({"error": "File not found"}), 404

    # Send file and delete it after download
    response = send_file(filepath, as_attachment=True)
    response.call_on_close(lambda: os.remove(filepath) if os.path.exists(filepath) else None)
    return response