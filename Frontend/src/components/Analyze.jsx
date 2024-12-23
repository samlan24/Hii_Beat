import React, { useState } from 'react';
import axios from 'axios';
import styles from './Analyze.module.css';

const AnalyzePage = () => {
  const [file, setFile] = useState(null);
  const [result, setResult] = useState(null);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleFileChange = (event) => {
    setFile(event.target.files[0]);
  };

  const handleSubmit = async (event) => {
    event.preventDefault();

    if (!file) {
      setError('Please upload a file.');
      setResult(null);
      return;
    }

    setLoading(true);
    setError('');
    setResult(null);

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
    } catch (err) {
      console.log('There was an error fetching the data:', err);
      setError(err.response?.data?.error || 'An error occurred');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className={styles.pageContainer}>
      <div className={styles.analyze}>
        <div className={styles.header}>
          <h1>Song Key & BPM Finder</h1>
          <p>
            Upload your audio files to find the key and tempo of the tracks in your library.
            This is a tool for DJs, producers, and anyone interested in understanding their music better.
          </p>
        </div>
        <form onSubmit={handleSubmit} className={styles.uploadForm}>
          <input type="file" onChange={handleFileChange} />
          <button type="submit" className={styles.submitButton} disabled={loading}>
            {loading ? 'Analyzing...' : 'Analyze'}
          </button>
        </form>
        <div className={styles.outputBox}>
          {loading && <div className={styles.loader}></div>}
          {!loading && error && <p className={styles.errorMessage}>{error}</p>}
          {!loading && result ? (
            <div className={styles.results}>
              <p><strong>BPM:</strong> {result.BPM}</p>
              <p><strong>Key:</strong> {result.Key}</p>
            </div>
          ) : (
            !loading && <p className={styles.placeholder}>Results will appear here after analysis.</p>
          )}
        </div>
      </div>
      <div className={styles.analyzeContent}>
        <h2>How to Use</h2>
        <p>Upload a song and click "Analyze" to get the key and BPM of the track.</p>
      </div>
    </div>
  );
};

export default AnalyzePage;
