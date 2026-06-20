def test_root_endpoint():
    from fastapi.testclient import TestClient
    from backend.main import app
    client = TestClient(app)
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to TradePilot AI API"}
