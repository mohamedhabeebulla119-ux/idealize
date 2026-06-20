import React from 'react';
import RiskCard from '../components/RiskCard';

function RiskAnalysis() {
  return (
    <div className="page risk-page">
      <h2>Trade Risk Analysis</h2>
      <p>Identify regulatory bottlenecks, sanctions, tariffs, and potential operational trade risks.</p>
      <RiskCard />
    </div>
  );
}

export default RiskAnalysis;
