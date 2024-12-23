import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import AnalyzePage from './components/Analyze';
import ConvertAudio from './components/Convert';
import GeneralNavbar from './components/GeneralNavbar';
import TopNavbar from './components/TopNavbar';


const App = () => {
  return (
    <Router>
      <div>
        <GeneralNavbar />
        <TopNavbar />
        <Routes>
          <Route exact path="/analyze" element={<AnalyzePage />} />
          <Route exact path="/convert" element={<ConvertAudio />} />
        </Routes>
      </div>
    </Router>
  );
};

export default App;
