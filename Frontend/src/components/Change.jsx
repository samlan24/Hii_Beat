import React, { useState } from 'react';
import axios from 'axios';
import styles from './Change.module.css';

const ChangeAudioPage = () => {
  const [file, setFile] = useState(null);
  const [transposeSteps, setTransposeSteps] = useState(0);
  const [result, setResult] = useState(null);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false); // New state for loading

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

    setLoading(true); // Start loading
    setError('');
    setResult(null);

    try {
      const response = await axios.post('http://localhost:5000/transpose', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
        withCredentials: true,
      });
      setResult(response.data);
    } catch (err) {
      console.error('There was an error processing the audio:', err);
      setError(err.response?.data?.error || 'An error occurred');
    } finally {
      setLoading(false); // Stop loading
    }
  };

  return (
    <div className={styles.pageContainer}>
      <div className={styles.analyze}>
        <header className={styles.header}>
          <h1>Transpose Audio</h1>
          <p>Upload your audio file and adjust the pitch easily.</p>
        </header>
        <form onSubmit={handleSubmit} className={styles.uploadForm}>
          <div>
            <label htmlFor="file" className={styles.label}>
              Select File:
            </label>
            <input
              id="file"
              type="file"
              accept="audio/mp3, audio/wav"
              onChange={handleFileChange}
              className={styles.fileInput}
            />
          </div>
          <div>
            <label htmlFor="steps" className={styles.label}>
              Transpose Steps (+/-):
            </label>
            <input
              id="steps"
              type="number"
              value={transposeSteps}
              onChange={(e) => setTransposeSteps(parseInt(e.target.value, 10))}
              className={styles.numberInput}
            />
          </div>
          <button
            type="submit"
            className={styles.submitButton}
            disabled={!file || loading} // Disable button when loading
          >
            {loading ? <div className={styles.loader}></div> : 'Transpose'}
          </button>
        </form>

        {error && <p className={styles.errorMessage}>{error}</p>}

        {result && (
          <div className={styles.outputBox}>
            {result.success ? (
              <div className={styles.results}>
                <p>Audio processed successfully!</p>
                <a
                  href={`http://localhost:5000${result.download_link}`}
                  download
                  className={styles.downloadLink}
                >
                  Download Modified Audio
                </a>
              </div>
            ) : (
              <p className={styles.errorMessage}>Processing failed. Try again.</p>
            )}
          </div>
        )}
      </div>
    </div>
  );
};

export default ChangeAudioPage;
