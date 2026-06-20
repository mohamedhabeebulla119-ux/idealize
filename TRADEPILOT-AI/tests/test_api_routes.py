import pytest

def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_intent_route(client):
    payload = {"query": "What are the rules for importing medical devices?"}
    response = client.post("/api/intent/", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "query" in data
    assert "final_response" in data

def test_workflow_route(client):
    payload = {"trade_type": "import", "product": "Medical Devices", "country": "Sri Lanka"}
    response = client.post("/api/workflow/", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "workflow" in data

def test_compliance_route(client):
    payload = {"trade_type": "import", "product": "Medical Devices", "country": "Sri Lanka"}
    response = client.post("/api/compliance/", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "documents" in data

def test_cost_estimation_route(client):
    payload = {"product": "Medical Devices", "country": "Sri Lanka", "product_value": 50000}
    response = client.post("/api/cost-estimation/", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "hs_code" in data
    assert "cost_breakdown" in data

def test_document_verification_vision_route(client):
    # Simulate a file upload for the vision endpoint
    dummy_file_content = b"DUMMY INVOICE PDF CONTENT"
    files = {"file": ("dummy.pdf", dummy_file_content, "application/pdf")}
    data = {
        "document_type": "Commercial Invoice",
        "expected_standards": "Must have a date."
    }
    response = client.post("/api/document-verification/", files=files, data=data)
    assert response.status_code == 200
    resp_data = response.json()
    assert "is_valid" in resp_data
    assert "errors" in resp_data
