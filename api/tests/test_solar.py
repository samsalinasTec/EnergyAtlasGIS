# OBJETIVO: validar el endpoint de análisis solar (modo dummy).
from fastapi.testclient import TestClient
from app.main import app


client = TestClient(app)


def test_solar_dummy_ok():
    payload = {
        "latitude": 19.4326,
        "longitude": -99.1332,
        "area_m2": 120,
        "panel_efficiency": 0.2,
        "performance_ratio": 0.8,
        "data_source": "dummy",
    }
    response = client.post("/api/solar/analyze", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["data_source"] == "dummy"
    assert data["annual_energy_kwh"] > 0
    assert len(data["monthly_energy_kwh"]) == 12
