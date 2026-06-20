import React from 'react';
import ReadinessScore from '../components/ReadinessScore';

function ReadinessReport() {
  return (
    <div className="page readiness-page">
      <h2>Trade Readiness Report</h2>
      <p>Calculate your compliance capability score based on requirements.</p>
      <ReadinessScore score={85} />
    </div>
  );
}

export default ReadinessReport;
