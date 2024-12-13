// src/components/ConvertAudio.jsx

import React, { useState } from 'react';
import axios from 'axios';
import styles from './Convert.module.css'


const ConvertAudio = () => {
    const [file, setFile] = useState(null);
    const [result, setResult] = useState(null);
    const [error, setError] = useState('');

    const handleFileChange = (event) => {
      setFile(event.target.files[0]);
    };

    const handleSubmit = async (event) => {
      event.preventDefault();

      if (!file) {
        setError('Please upload a file.');
        return;
      }

      const formData = new FormData();
      formData.append('file', file);

      try {
        const response = await axios.post('http://localhost:5000/convert', formData, {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
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
      <div className={styles.convert}>
        <h1>Convert MP3 to WAV</h1>
        <form onSubmit={handleSubmit}>
          <input type="file" accept="audio/mp3" onChange={handleFileChange} />
          <button type="submit">Convert Audio</button>
        </form>

        {error && <p style={{ color: 'red' }}>{error}</p>}
        {result && result.success && (
          <div>
            <p>Audio converted successfully!</p>
            <a href={`http://localhost:5000${result.download_link}`} download>
              Download Converted WAV
            </a>
          </div>
        )}
      </div>
    );
  };

  export default ConvertAudio;