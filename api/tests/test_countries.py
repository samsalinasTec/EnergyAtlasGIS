# OBJETIVO: prueba rápida (evita romper endpoints sin querer).
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_list_ok():
    r = client.get("/api/paises")
    assert r.status_code == 200
    assert isinstance(r.json(), list)

def test_ficha_404():
    r = client.get("/api/paises/XXX/ficha")
    assert r.status_code == 404
