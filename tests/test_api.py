from fastapi.testclient import TestClient
from src.api.app import app
client = TestClient(app)
def test_home():
    assert client.get("/").status_code == 200
def test_health():
    assert client.get("/health").status_code == 200
def test_ask():
    r = client.post("/ask", json={"question": "What is revenue?"})
    assert r.status_code == 200
    assert "answer" in r.json()
