import React, { useState } from 'react';
import axios from 'axios';
import styles from './Convert.module.css';

const ConvertAudio = () => {
  const [file, setFile] = useState(null);
  const [targetFormat, setTargetFormat] = useState('mp3'); // Default target format
  const [result, setResult] = useState(null);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleFileChange = (event) => {
    setFile(event.target.files[0]);
  };

  const handleFormatChange = (event) => {
    setTargetFormat(event.target.value);
  };

  const handleSubmit = async (event) => {
    event.preventDefault();

    if (!file) {
      setError('Please upload a file.');
      return;
    }

    setLoading(true);
    setError('');
    setResult(null);

    const formData = new FormData();
    formData.append('file', file);
    formData.append('target_format', targetFormat); // Send target format to the backend

    try {
      const response = await axios.post('http://localhost:5000/convert', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
        withCredentials: true,
      });
      setResult(response.data);
    } catch (err) {
      console.error('There was an error converting the audio:', err);
      setError(err.response?.data?.error || 'An error occurred');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className={styles.pageContainer}>
      <div className={styles.convert}>
        <h1>Convert Audio Files</h1>
        <p className={styles.fileInfo}>
          Upload audio files in formats like <strong>MP3, WAV, FLAC, AAC,</strong> and more. Convert them to your desired format in just a few clicks!
        </p>
        <form onSubmit={handleSubmit} className={styles.convertForm}>
          <input
            type="file"
            accept="audio/*"
            onChange={handleFileChange}
          />
          <div className={styles.formatSelector}>
            <label htmlFor="format">Select target format:</label>
            <select
              id="format"
              value={targetFormat}
              onChange={handleFormatChange}
            >
              <option value="mp3">MP3</option>
              <option value="wav">WAV</option>
              <option value="flac">FLAC</option>
              <option value="aac">AAC</option>
              <option value="ogg">OGG</option>
            </select>
          </div>
          <button type="submit" className={styles.submitButton} disabled={loading}>
            {loading ? 'Converting...' : 'Convert Audio'}
          </button>
        </form>
        <div className={styles.outputBox}>
          {loading && <div className={styles.loader}></div>}
          {error && <p className={styles.errorMessage}>{error}</p>}
          {result && result.success && (
            <div>
              <p className={styles.successMessage}>Audio converted successfully!</p>
              <a
                href={`http://localhost:5000${result.download_link}`}
                download
                className={styles.downloadLink}
              >
                Download Converted {targetFormat.toUpperCase()}
              </a>
            </div>
          )}
        </div>
      </div>
      <div className={styles.convertContent}>
        <h2>How to Use</h2>
        <p>Upload an audio file, choose the desired format, and click "Convert Audio" to get your converted file.</p>
      </div>
    </div>
  );
};

export default ConvertAudio;
