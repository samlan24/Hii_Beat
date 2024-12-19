// FILE: components/TopNavbar.jsx
import React from 'react';
import { Link } from 'react-router-dom';
import styles from './TopNavbar.module.css';

const TopNavbar = () => {
  return (
    <nav className={styles.navbar}>
      <ul>
        <li><Link to="/analyze">Bpm&Key</Link></li>
        <li><Link to="/change">Transpose</Link></li>
        <li><Link to="/convert">Convert</Link></li>
      </ul>
    </nav>
  );
};

export default TopNavbar;