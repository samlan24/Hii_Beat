import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import AnalyzePage from './components/Analyze';
import ConvertAudio from './components/Convert';
import TopNavbar from './components/TopNavbar';
import LandingPage from './components/LandingPage';


const App = () => {
  return (
    <Router>
      <div>
        <TopNavbar />
        <Routes>
          <Route exact path="/analyze" element={<AnalyzePage />} />
          <Route exact path="/convert" element={<ConvertAudio />} />
          <Route path="/" element={<LandingPage />} />
        </Routes>
      </div>
    </Router>
  );
};

export default App;
