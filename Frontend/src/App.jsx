// src/App.jsx
import React, { useState } from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import AnalyzePage from './components/Analyze';
import ChangeBpmPage from './components/Change';
import ConvertAudio from './components/Convert';


const App = () => {
  return (
    <Router>
      <Routes>
        <Route exact path="/analyze" element={<AnalyzePage />} />
        <Route exact path="/change" element={<ChangeBpmPage />} />
        <Route exact path="/convert" element={<ConvertAudio />} />
      </Routes>
    </Router>
  );
};

export default App;