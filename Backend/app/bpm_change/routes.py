import os
from flask import Blueprint, request, jsonify, send_file, current_app
import librosa
import soundfile as sf
from pydub import AudioSegment

from . import bpm_change

@bpm_change.route('/transpose', methods=['POST'])
def transpose():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files['file']

    # Check if the uploaded file is an audio file (MP3 or WAV)
    if not (file.filename.endswith('.mp3') or file.filename.endswith('.wav')):
        return jsonify({"error": "Invalid file type. Only MP3 and WAV files are allowed."}), 400

    transpose_steps = int(request.form.get('transpose_steps', 0))  # Default to no transposition

    # Save uploaded audio file temporarily
    uploaded_filename = os.path.join(current_app.config['UPLOAD_FOLDER'], file.filename)
    file.save(uploaded_filename)

    try:
        # Process the file with Librosa
        y, sr = librosa.load(uploaded_filename, sr=None)

        # Transpose the audio by the specified number of semitones (no BPM change)
        y_transposed = librosa.effects.pitch_shift(y, sr=sr, n_steps=transpose_steps)

        # Output file name and path
        output_filename = os.path.splitext(file.filename)[0] + '_transposed' + os.path.splitext(file.filename)[1]
        output_filepath = os.path.join(current_app.config['CONVERT_FOLDER'], output_filename)

        # Save the modified file
        if file.filename.endswith('.wav'):
            sf.write(output_filepath, y_transposed, sr, format='WAV')
        elif file.filename.endswith('.mp3'):
            # Convert the WAV result to MP3 using pydub (avoid lossy re-encoding from MP3 to MP3)
            temp_wav = os.path.join(current_app.config['CONVERT_FOLDER'], 'temp.wav')
            sf.write(temp_wav, y_transposed, sr, format='WAV')
            # Use pydub to convert WAV to MP3 without loss in quality
            audio = AudioSegment.from_wav(temp_wav)
            audio.export(output_filepath, format='mp3')
            os.remove(temp_wav)  # Clean up the temporary WAV file

    except Exception as e:
        return jsonify({"error": f"Error transposing audio: {e}"}), 500

    finally:
        # Cleanup: Remove the uploaded audio file after processing
        if os.path.exists(uploaded_filename):
            os.remove(uploaded_filename)

    return jsonify({"success": True, "download_link": f"/download/{output_filename}"})


@bpm_change.route('/download/<filename>', methods=['GET'])
def download(filename):
    filepath = os.path.join(current_app.config['CONVERT_FOLDER'], filename)
    if not os.path.exists(filepath):
        return jsonify({"error": "File not found"}), 404

    return send_file(filepath, as_attachment=True)
