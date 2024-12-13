import React, { useState } from 'react';
import axios from 'axios';

const AudioSeparator = () => {
  const [file, setFile] = useState(null);
  const [vocalLink, setVocalLink] = useState('');
  const [accompanimentLink, setAccompanimentLink] = useState('');
  const [error, setError] = useState('');

  const handleFileChange = (event) => {
    setFile(event.target.files[0]);
  };

  const handleUpload = async () => {
    if (!file) {
      setError('Please upload a file first.');
      return;
    }

    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await axios.post('/spleet', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });

      if (response.data.success) {
        setVocalLink(response.data.vocal_download_link);
        setAccompanimentLink(response.data.accompaniment_download_link);
        setError('');
      }
    } catch (err) {
      setError('Error during separation. Please try again.');
    }
  };

  return (
    <div>
      <h1>Audio Separator</h1>
      <input type="file" accept=".mp3,.wav" onChange={handleFileChange} />
      <button onClick={handleUpload}>Upload and Separate</button>

      {vocalLink && (
        <div>
          <a href={vocalLink} download>
            Download Vocals
          </a>
        </div>
      )}
      {accompanimentLink && (
        <div>
          <a href={accompanimentLink} download>
            Download Instrumentals
          </a>
        </div>
      )}
      {error && <p style={{ color: 'red' }}>{error}</p>}
    </div>
  );
};

export default AudioSeparator;
