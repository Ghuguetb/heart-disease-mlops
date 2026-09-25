# Heart Disease MLOps

Proyecto integrador de Machine Learning Operations: un modelo de clasificación que predice el riesgo de enfermedad cardíaca, llevado a través de un ciclo completo de MLOps — desde el análisis exploratorio hasta el despliegue en Kubernetes, integración continua y monitoreo de deriva de datos.

Dataset: [Heart Failure Prediction Dataset](https://www.kaggle.com/datasets/fedesoriano/heart-failure-prediction) (Kaggle), 918 pacientes, 11 variables clínicas.

## Resultados

Comparación de 5 modelos (Pipeline + GridSearchCV, validación cruzada de 5 folds):

| Modelo | AUC | Accuracy |
|---|---|---|
| Regresión Logística | 0.931 | 0.864 |
| Gradient Boosting | 0.930 | 0.864 |
| Random Forest | 0.930 | 0.853 |
| SVC | 0.929 | 0.842 |
| KNN | 0.917 | 0.837 |

Modelo final: **Regresión Logística** (`C=1`), evaluado sobre un conjunto de prueba independiente (184 pacientes, nunca usados en entrenamiento):
- AUC: 0.931
- Accuracy: 0.864
- Sensibilidad: 85.0%
- Especificidad: 88.3%

## Estructura del proyecto

heart-disease-mlops/
├── app/
│ ├── api.py # API de FastAPI
│ └── model.joblib # Modelo entrenado (Pipeline completo)
├── docker/
│ ├── Dockerfile
│ └── requirements.txt
├── k8s/
│ ├── deployment.yaml
│ └── service.yaml
├── notebooks/
│ ├── 1_model_leakage_demo.ipynb # Exploracion, data leakage, comparacion de 5 modelos
│ ├── 2_model_pipeline_cv.ipynb # Pipeline final, evaluacion, exportacion del modelo
│ └── 3_data_drift_monitoring.ipynb # Reporte de data drift con Evidently
├── tests/
│ └── test_api.py
├── .github/workflows/
│ └── ci.yml # Integracion continua (lint + tests)
├── data/
│ └── heart.csv
├── drift_report.html # Reporte de monitoreo generado
└── README.md


## Cómo correrlo

Requisitos: Python 3.13, Docker Desktop, Minikube, kubectl.

### 1. Notebooks (análisis y entrenamiento)

Abrir `notebooks/1_model_leakage_demo.ipynb` y `notebooks/2_model_pipeline_cv.ipynb` en Jupyter o VS Code y ejecutar en orden. El segundo notebook exporta el modelo entrenado a `app/model.joblib`.

### 2. API localmente (sin Docker)

```bash
pip install fastapi uvicorn pydantic joblib pandas scikit-learn
uvicorn app.api:app --reload
```

Probar en `http://127.0.0.1:8000/docs`.

### 3. Docker

```bash
docker build -t heart-api -f docker/Dockerfile .
docker run -p 8000:8000 heart-api
```

### 4. Kubernetes (Minikube)

```bash
minikube start --driver=docker
minikube image load heart-api:latest
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
minikube service heart-service
```

### 5. Integración continua

El workflow en `.github/workflows/ci.yml` corre automáticamente en cada `push`: instala dependencias, revisa estilo con `flake8` y ejecuta las pruebas con `pytest`.

### 6. Monitoreo de data drift

Generado en `notebooks/3_data_drift_monitoring.ipynb`, comparando la distribución de `X_train` (referencia) contra `X_test` (datos "actuales"). Resultado: sin drift significativo a nivel de dataset (1 de 11 columnas con drift individual — `Sex`, explicable por el desbalance natural de esa variable en el dataset original).

## Ejemplo de uso de la API

```bash
curl -X POST http://127.0.0.1:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "Age": 58, "Sex": "M", "ChestPainType": "ASY",
    "RestingBP": 140, "Cholesterol": 289, "FastingBS": 0,
    "RestingECG": "Normal", "MaxHR": 120, "ExerciseAngina": "Y",
    "Oldpeak": 2.5, "ST_Slope": "Flat"
  }'
```

Respuesta:
```json
{"heart_disease_probability": 0.9597, "prediction": 1}
```

## Notas sobre la implementación

El material de referencia del curso incluye un ejemplo de código de carácter general. Para adaptarlo al dataset específico utilizado en este proyecto, se realizaron los siguientes ajustes:

1. La columna objetivo en este dataset se llama `HeartDisease`.
2. Al incluir el dataset variables categóricas de texto, se incorporó un `OneHotEncoder` dentro de un `ColumnTransformer`.
3. Se identificó que `Cholesterol` y `RestingBP` registran valores en `0` que corresponden a datos no disponibles; se manejan como valores faltantes e imputan con la mediana dentro del pipeline.
4. En la demostración de data leakage, se ajustó el orden de las transformaciones para que la comparación entre el flujo correcto y el flujo con fuga resultara representativa.
5. Los hiperparámetros de `GridSearchCV` se referencian con el prefijo del paso correspondiente del pipeline (por ejemplo, `clf__C`).
6. El modelo se guarda en `app/model.joblib`, ruta que coincide con la que utiliza `api.py`.
7. La API recibe los datos como un objeto estructurado (modelo `Paciente` de Pydantic), con los nombres de columna del dataset.
8. El despliegue en Kubernetes utiliza la imagen construida localmente (`imagePullPolicy: Never`), cargada con `minikube image load`.
9. Se añadió la carpeta `tests/` con una prueba de la API, utilizada por el workflow de integración continua.
10. Se utilizó la versión actual de la librería Evidently (`evidently.Report`, `evidently.presets.DataDriftPreset`), dado que su forma de uso cambió respecto a versiones anteriores.
