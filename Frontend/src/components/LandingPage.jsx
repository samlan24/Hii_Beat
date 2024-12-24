import React from 'react';
import { Link } from 'react-router-dom';
import styles from './LandingPage.module.css';
import analyzeImage from '../assets/dj.jpg';
import convertImage from '../assets/dj2.jpg';
import searchImage from '../assets/viny.jpg';

const LandingPage = () => {
  return (
    <div className={styles.landing}>
      <header className={styles.header}>
        <h1>Welcome to HiiBeat</h1>
        <p>Your go-to platform for audio analysis and conversion powered by cutting-edge technology.</p>
      </header>

      {/* Analyze Section */}
      <section className={`${styles.featureSection} ${styles.reverse}`}>
        <div className={styles.content}>
          <h2 className={styles.sectionTitle}>Analyze Songs</h2>
          <ol className={styles.steps}>
            <li className={styles.step}>
              <span className={styles.stepNumber}>1</span>
              Add an audio file (MP3, WAV, or AAC).
            </li>
            <li className={styles.step}>
              <span className={styles.stepNumber}>2</span>
              Let the app process your audio.
            </li>
            <li className={styles.step}>
              <span className={styles.stepNumber}>3</span>
              Get detailed insights like BPM, key.
            </li>
          </ol>
          <Link to="/analyze" className={styles.link}>Start Analyzing</Link>
        </div>
        <div className={styles.imageWrapper}>
          <img src={analyzeImage} alt="Analyze Audio" className={styles.image} />
        </div>
      </section>

      {/* Convert Section */}
      <section className={styles.featureSection}>
        <div className={styles.imageWrapper}>
          <img src={convertImage} alt="Convert Audio" className={styles.image} />
        </div>
        <div className={styles.content}>
          <h2 className={styles.sectionTitle}>Convert Audio Formats</h2>
          <ol className={styles.steps}>
            <li className={styles.step}>
              <span className={styles.stepNumber}>1</span>
              Upload an audio file.
            </li>
            <li className={styles.step}>
              <span className={styles.stepNumber}>2</span>
              Let the app convert the audio.
            </li>
            <li className={styles.step}>
              <span className={styles.stepNumber}>3</span>
              Download the converted file instantly.
            </li>
          </ol>
          <Link to="/convert" className={styles.link}>Convert Now</Link>
        </div>
      </section>

      {/* Search Section */}
      <section className={`${styles.featureSection} ${styles.reverse}`}>
        <div className={styles.content}>
          <h2 className={styles.sectionTitle}>Change Pitch</h2>
          <ol className={styles.steps}>
            <li className={styles.step}>
              <span className={styles.stepNumber}>1</span>
              Add an audio file (MP3, WAV, or AAC)
            </li>
            <li className={styles.step}>
              <span className={styles.stepNumber}>2</span>
              Let the app process the audio
            </li>
            <li className={styles.step}>
              <span className={styles.stepNumber}>3</span>
              Download the transposed song
            </li>
          </ol>
          <Link to="/change" className={styles.link}>Change Now</Link>
        </div>
        <div className={styles.imageWrapper}>
          <img src={searchImage} alt="change BPM" className={styles.image} />
        </div>
      </section>

      <footer className={styles.footer}>
        <p>Experience professional-grade audio tools. Join HiiBeat today!</p>
      </footer>
    </div>
  );
};

export default LandingPage;
