import React from 'react';

function ReadinessScore({ score }) {
  return (
    <div className="readiness-score-card">
      <h3>Compliance Readiness Score</h3>
      <div className="score-radial" style={{ fontSize: '2rem', margin: '20px' }}>
        {score}%
      </div>
      <p>{score >= 80 ? 'Good to go!' : 'Requires Attention.'}</p>
    </div>
  );
}

export default ReadinessScore;
