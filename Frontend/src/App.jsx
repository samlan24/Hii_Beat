import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Route, Routes, Navigate } from 'react-router-dom';
import AnalyzePage from './components/Analyze';
import ChangeBpmPage from './components/Change';
import ConvertAudio from './components/Convert';
import TopNavbar from './components/TopNavbar';


const App = () => {
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  useEffect(() => {
    // Check if the user is authenticated (e.g., by checking a token in sessionStorage)
    const user = sessionStorage.getItem('user');
    if (user) {
      setIsAuthenticated(true);
    }
  }, []);

  return (
    <Router>
      <div>
        <TopNavbar />
        <Routes>
          <Route path="/analyze" element={<AnalyzePage />} />
          <Route path="/change" element={<ChangeBpmPage />} />
          <Route path="/convert" element={<ConvertAudio />} />
        </Routes>
      </div>
    </Router>
  );
};

export default App;