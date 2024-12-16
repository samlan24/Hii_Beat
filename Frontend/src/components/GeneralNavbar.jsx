// FILE: components/GeneralNavbar.jsx
import React from 'react';
import { Link } from 'react-router-dom';
import styles from './GeneralNavbar.module.css';

const GeneralNavbar = () => {
  return (
    <nav className={styles.navbar}>
      <ul>
        <li><Link to="/blog">Blog</Link></li>
        <li><Link to="/contact">Contact</Link></li>
      </ul>
    </nav>
  );
};

export default GeneralNavbar;