// FILE: components/TopNavbar.jsx
import React from 'react';
import { Link } from 'react-router-dom';
import styles from './TopNavbar.module.css';

const TopNavbar = () => {
  return (
    <nav className={styles.navbar}>
      <ul>
        <li><Link to="/analyze">Analyze</Link></li>
        <li><Link to="/change">Change BPM</Link></li>
        <li><Link to="/convert">Convert Audio</Link></li>
      </ul>
    </nav>
  );
};

export default TopNavbar;