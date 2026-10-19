from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health():
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

def test_knowledge_has_sources():
    response = client.post("/api/knowledge/ask", json={"question": "How does soil pH affect crops?"})
    assert response.status_code == 200
    assert "answer" in response.json()
    assert isinstance(response.json()["sources"], list)

def test_invalid_input_rejected():
    response = client.post("/api/predict", json={
        "N": -1, "P": 40, "K": 40, "temperature": 25,
        "humidity": 70, "ph": 6.5, "rainfall": 100
    })
    assert response.status_code == 422
