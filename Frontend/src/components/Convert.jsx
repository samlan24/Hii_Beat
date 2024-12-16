import React, { useState } from 'react';
import axios from 'axios';
import styles from './Convert.module.css'

const ConvertAudio = () => {
  const [file, setFile] = useState(null);
  const [targetFormat, setTargetFormat] = useState('mp3'); // Default target format
  const [result, setResult] = useState(null);
  const [error, setError] = useState('');

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
      setError('');
    } catch (err) {
      console.error('There was an error converting the audio:', err);
      setError(err.response?.data?.error || 'An error occurred');
      setResult(null);
    }
  };

  return (
    <div>
      <div className={styles.convert}>
        <h1>Convert Audio Files</h1>
        <form onSubmit={handleSubmit}>
          <input
            type="file"
            accept="audio/*"
            onChange={handleFileChange}
          />
          <div>
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
          <button type="submit">Convert Audio</button>
        </form>

        {error && <p style={{ color: 'red' }}>{error}</p>}
        {result && result.success && (
          <div>
            <p>Audio converted successfully!</p>
            <a href={`http://localhost:5000${result.download_link}`} download>
              Download Converted {targetFormat.toUpperCase()}
            </a>
          </div>
        )}
      </div>
      <div className={styles.convertContent}>
        <h2>What to do</h2>
      </div>
    </div>
  );
};

export default ConvertAudio;
