const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api';

export async function sendQuery(query) {
  const response = await fetch(`${API_BASE_URL}/query/`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ query }),
  });
  return response.json();
}

export async function getWorkflow(workflowId) {
  const response = await fetch(`${API_BASE_URL}/workflow/${workflowId}`);
  return response.json();
}

export async function getCompliance(query) {
  const response = await fetch(`${API_BASE_URL}/compliance/`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ query }),
  });
  return response.json();
}

export async function getRiskAnalysis(query) {
  const response = await fetch(`${API_BASE_URL}/risk/`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ query }),
  });
  return response.json();
}

export async function getChecklist(query) {
  const response = await fetch(`${API_BASE_URL}/checklist/`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ query }),
  });
  return response.json();
}
