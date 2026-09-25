from fastapi.testclient import TestClient
from app.api import app

client = TestClient(app)

def test_predict_devuelve_prediccion_valida():
    paciente = {
        "Age": 58,
        "Sex": "M",
        "ChestPainType": "ASY",
        "RestingBP": 140,
        "Cholesterol": 289,
        "FastingBS": 0,
        "RestingECG": "Normal",
        "MaxHR": 120,
        "ExerciseAngina": "Y",
        "Oldpeak": 2.5,
        "ST_Slope": "Flat"
    }

    respuesta = client.post("/predict", json=paciente)

    assert respuesta.status_code == 200
    datos = respuesta.json()
    assert "heart_disease_probability" in datos
    assert "prediction" in datos
    assert 0 <= datos["heart_disease_probability"] <= 1
    assert datos["prediction"] in [0, 1]
    