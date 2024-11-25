// src/components/ChangeAudio.jsx

import React, { useState } from 'react';
import axios from 'axios';
import styles from './Change.module.css'


const ChangeBpmPage = () => {
  const [file, setFile] = useState(null);
  const [bpmFactor, setBpmFactor] = useState(1.0);
  const [pitchSteps, setPitchSteps] = useState(0);
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
    formData.append('bpm_factor', bpmFactor);
    formData.append('pitch_steps', pitchSteps);

    try {
      const response = await axios.post('http://localhost:5000/change', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      setResult(response.data);
      setError('');
    } catch (err) {
      console.error('There was an error processing the audio:', err);
      setError(err.response?.data?.error || 'An error occurred');
      setResult(null);
    }
  };

  return (
    <div>
      <h1 className={styles.heading}>Change Audio BPM and Pitch</h1>
      <form onSubmit={handleSubmit}>
        <input type="file" accept="audio/*" onChange={handleFileChange} />
        <div>
          <label>BPM Factor:</label>
          <input
            type="number"
            step="0.1"
            value={bpmFactor}
            onChange={(e) => setBpmFactor(parseFloat(e.target.value))}
          />
        </div>
        <div>
          <label>Pitch Steps:</label>
          <input
            type="number"
            value={pitchSteps}
            onChange={(e) => setPitchSteps(parseInt(e.target.value))}
          />
        </div>
        <button type="submit">Change Audio</button>
      </form>

      {error && <p style={{ color: 'red' }}>{error}</p>}
      {result && result.success && (
        <div>
          <p>Audio processed successfully!</p>
          <a href={`http://localhost:5000${result.download_link}`} download>
            Download Modified Audio
          </a>
        </div>
      )}
    </div>
  );
};

export default ChangeBpmPage;