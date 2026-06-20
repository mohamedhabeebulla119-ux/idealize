import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Home from './pages/Home';
import ImportExportPlanner from './pages/ImportExportPlanner';
import RiskAnalysis from './pages/RiskAnalysis';
import ReadinessReport from './pages/ReadinessReport';
import ChecklistPage from './pages/ChecklistPage';

function App() {
  return (
    <Router>
      <div className="app-container">
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/planner" element={<ImportExportPlanner />} />
          <Route path="/risk" element={<RiskAnalysis />} />
          <Route path="/readiness" element={<ReadinessReport />} />
          <Route path="/checklist" element={<ChecklistPage />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
