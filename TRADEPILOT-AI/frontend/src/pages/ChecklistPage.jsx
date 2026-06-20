import React from 'react';
import ChecklistCard from '../components/ChecklistCard';

function ChecklistPage() {
  return (
    <div className="page checklist-page">
      <h2>Compliance Checklist</h2>
      <p>Verify document status, permits, and declarations before submitting cargo.</p>
      <ChecklistCard />
    </div>
  );
}

export default ChecklistPage;
