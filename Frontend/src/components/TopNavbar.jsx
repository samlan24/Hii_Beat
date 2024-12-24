// FILE: components/TopNavbar.jsx
import React from 'react';
import { Link } from 'react-router-dom';
import styles from './TopNavbar.module.css';

const TopNavbar = () => {
  return (
    <nav className={styles.navbar}>
      <ul>
        <li><Link to="/">Home</Link></li>
        <li><Link to="/analyze">Bpm&key</Link></li>
        <li><Link to="/convert">Audio Converter</Link></li>
        <li><Link to="/change">Change Pitch</Link></li>
      </ul>
    </nav>
  );
};

export default TopNavbar;