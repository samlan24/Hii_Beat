import React, { useState } from 'react';
import axios from 'axios';
import styles from './Change.module.css';

const ChangeAudioPage = () => {
  const [file, setFile] = useState(null);
  const [transposeSteps, setTransposeSteps] = useState(0);  // Default to no transpose
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
    formData.append('transpose_steps', transposeSteps);

    try {
      const response = await axios.post('http://localhost:5000/transpose', formData, {
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
    <div className={styles.change}>
      <h1 className={styles.heading}>Transpose Audio</h1>
      <form onSubmit={handleSubmit}>
        <input type="file" accept="audio/mp3, audio/wav" onChange={handleFileChange} />
        <div>
          <label>Transpose Steps (+/-):</label>
          <input
            type="number"
            value={transposeSteps}
            onChange={(e) => setTransposeSteps(parseInt(e.target.value))}
          />
        </div>
        <button type="submit">Transpose Audio</button>
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

export default ChangeAudioPage;
