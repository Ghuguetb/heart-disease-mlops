from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import pandas as pd

modelo = joblib.load("app/model.joblib")

app = FastAPI()

class Paciente(BaseModel):
    Age: int
    Sex: str
    ChestPainType: str
    RestingBP: float
    Cholesterol: float
    FastingBS: int
    RestingECG: str
    MaxHR: int
    ExerciseAngina: str
    Oldpeak: float
    ST_Slope: str

@app.post("/predict")
def predict(paciente: Paciente):
    datos = pd.DataFrame([paciente.dict()])
    proba = modelo.predict_proba(datos)[0][1]
    return {
        "heart_disease_probability": float(proba),
        "prediction": int(proba > 0.5)
    }

