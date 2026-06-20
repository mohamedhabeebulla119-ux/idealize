import React from 'react';
import ChatInterface from '../components/ChatInterface';

function Home() {
  return (
    <div className="page home-page">
      <h1>TradePilot AI - Trade Compliance & Planning</h1>
      <p>Analyze compliance risks, plan import/export workflows, and check trade readiness.</p>
      <ChatInterface />
    </div>
  );
}

export default Home;
