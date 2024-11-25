// src/components/AnalyzePage.jsx

import React, { useState } from 'react';
import axios from 'axios';
import './Analyze.module.css'

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
      <h1 className='heading'>BPM Analysis</h1>
      <form onSubmit={handleSubmit}>
        <input type="file" onChange={handleFileChange} />
        <button type="submit">Analyze</button>
      </form>
      {error && <p style={{ color: 'red' }}>{error}</p>}
      {result && (
        <div>
          <p>BPM: {result.BPM}</p>
          <p>Key: {result.Key}</p>
        </div>
      )}
    </div>
  );
};

export default AnalyzePage;