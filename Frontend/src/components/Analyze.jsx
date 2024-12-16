// src/components/AnalyzePage.jsx

import React, { useState } from 'react';
import axios from 'axios';
import styles from './Analyze.module.css'

const AnalyzePage = () => {
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
      const response = await axios.post('http://localhost:5000/analyze', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
        withCredentials: true,
      });
      setResult(response.data);
      setError('');
    } catch (err) {
      console.log('There was an error fetching the data:', err);
      setError(err.response?.data?.error || 'An error occurred');
      setResult(null);
    }
  };

  return (
    <div>
      <div className={styles.analyze}>
        <div>
        <h1>Song Key & BPM Finder</h1>
        <p>Upload your audio files to find the key and tempo of the tracks in your library.
          This is a tool for DJs interested in harmonic mixing,
          producers looking to remix songs, and anyone trying to understand their music a little better. </p>
        </div>
        <form onSubmit={handleSubmit}>
          <input type="file" onChange={handleFileChange} />
          <button type="submit">Analyze</button>
        </form>
        {error && <p style={{ color: 'red' }}>{error}</p>}
        {result && (
          <div className={styles.results}>
            <p>BPM: {result.BPM}</p>
            <p>Key: {result.Key}</p>
          </div>
        )}
      </div>
      <div className={styles.analyzeContent}>
        <h2>what to do</h2>
      </div>
    </div>
  );
};

export default AnalyzePage;