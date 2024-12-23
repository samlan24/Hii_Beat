import React from 'react';
import { Link } from 'react-router-dom';
import styles from './LandingPage.module.css';

const LandingPage = () => {
  return (
    <div className={styles.landing}>
      <header className={styles.header}>
        <h1>Welcome to HiiBeat</h1>
        <p>Your go-to platform for audio analysis and conversion powered by cutting-edge technology.</p>
      </header>

      <section className={styles.featureSection}>
        <h2 className={styles.sectionTitle}>Analyze Songs</h2>
        <ol className={styles.steps}>
          <li className={styles.step}>
            <span className={styles.stepNumber}>1</span>
            Add an audio file (MP3, WAV, or AAC) to the app.
          </li>
          <li className={styles.step}>
            <span className={styles.stepNumber}>2</span>
            Let the app process your audio using advanced algorithms.
          </li>
          <li className={styles.step}>
            <span className={styles.stepNumber}>3</span>
            Get detailed insights like BPM, key, and camelot numbers.
          </li>
        </ol>
        <Link to="/analyze" className={styles.link}>Start Analyzing</Link>
      </section>

      <section className={styles.featureSection}>
        <h2 className={styles.sectionTitle}>Convert Audio Formats</h2>
        <ol className={styles.steps}>
          <li className={styles.step}>
            <span className={styles.stepNumber}>1</span>
            Upload an audio file in any popular format (MP3, WAV, FLAC).
          </li>
          <li className={styles.step}>
            <span className={styles.stepNumber}>2</span>
            Let the app convert it to your desired format.
          </li>
          <li className={styles.step}>
            <span className={styles.stepNumber}>3</span>
            Download the converted file instantly.
          </li>
        </ol>
        <Link to="/convert" className={styles.link}>Convert Now</Link>
      </section>

      <section className={styles.featureSection}>
        <h2 className={styles.sectionTitle}>Search Songs</h2>
        <ol className={styles.steps}>
          <li className={styles.step}>
            <span className={styles.stepNumber}>1</span>
            Enter the name of the song or artist.
          </li>
          <li className={styles.step}>
            <span className={styles.stepNumber}>2</span>
            Let the app fetch song details from Spotify.
          </li>
          <li className={styles.step}>
            <span className={styles.stepNumber}>3</span>
            Get BPM, key, and camelot numbers for your searched track.
          </li>
        </ol>
        <Link to="/search" className={styles.link}>Search Songs</Link>
      </section>

      <footer className={styles.footer}>
        <p>Experience professional-grade audio tools. Join HiiBeat today!</p>
      </footer>
    </div>
  );
};

export default LandingPage;
