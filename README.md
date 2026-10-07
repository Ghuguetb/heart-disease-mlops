# Heart Disease MLOps

Tarea 2 del curso de Machine Learning, Maestría en Ingeniería Biomédica, Universidad del Norte.

Este proyecto lo hicimos Santiago Díaz, Gina Huguet y Leiry Mares.

Este es un proyecto integrador de Machine Learning Operations. Construimos un modelo de clasificación que predice el riesgo de enfermedad cardíaca y lo llevamos por todo el ciclo de MLOps, desde el análisis exploratorio hasta el despliegue en Kubernetes, pasando por integración continua y monitoreo de deriva de datos.

Usamos el [Heart Failure Prediction Dataset](https://www.kaggle.com/datasets/fedesoriano/heart-failure-prediction) de Kaggle, que tiene 918 pacientes y 11 variables clínicas.

## Resultados

Comparamos 5 modelos usando Pipeline y GridSearchCV, con validación cruzada de 5 folds.

| Modelo | AUC | Accuracy |
|---|---|---|
| Regresión Logística | 0.931 | 0.864 |
| Gradient Boosting | 0.930 | 0.864 |
| Random Forest | 0.930 | 0.853 |
| SVC | 0.929 | 0.842 |
| KNN | 0.917 | 0.837 |

Nos quedamos con la Regresión Logística (`C=1`) como modelo final. La evaluamos sobre un conjunto de prueba independiente, con 184 pacientes que nunca se usaron en el entrenamiento, y estos fueron los resultados.

- AUC de 0.931
- Accuracy de 0.864
- Sensibilidad de 85.0%
- Especificidad de 88.3%

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

Para correr esto necesitas Python 3.13, Docker Desktop, Minikube y kubectl.

### 1. Notebooks (análisis y entrenamiento)

Abre `notebooks/1_model_leakage_demo.ipynb` y `notebooks/2_model_pipeline_cv.ipynb` en Jupyter o VS Code y ejecútalos en orden. El segundo notebook exporta el modelo entrenado a `app/model.joblib`.

### 2. API localmente (sin Docker)

```bash
pip install fastapi uvicorn pydantic joblib pandas scikit-learn
uvicorn app.api:app --reload
```

Puedes probarla en `http://127.0.0.1:8000/docs`.

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

El workflow en `.github/workflows/ci.yml` corre automáticamente en cada `push`. Instala las dependencias, revisa el estilo con `flake8` y ejecuta las pruebas con `pytest`.

### 6. Monitoreo de data drift

Esto lo hicimos en `notebooks/3_data_drift_monitoring.ipynb`, comparando la distribución de `X_train` como referencia contra `X_test` como si fueran los datos actuales. No encontramos drift significativo a nivel de todo el dataset. Solo una de las 11 columnas mostró drift individual, `Sex`, y esto se explica por el desbalance natural que tiene esa variable en el dataset original.

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

Esto es lo que devuelve.
```json
{"heart_disease_probability": 0.9597, "prediction": 1}
```

## Notas sobre la implementación

El material de referencia del curso trae un ejemplo de código general. Para adaptarlo al dataset que usamos en este proyecto, hicimos varios ajustes.

1. La columna objetivo en este dataset se llama `HeartDisease`.
2. Como el dataset tiene variables categóricas de texto, incorporamos un `OneHotEncoder` dentro de un `ColumnTransformer`.
3. Nos dimos cuenta de que `Cholesterol` y `RestingBP` tienen valores en `0` que en realidad corresponden a datos no disponibles, así que los tratamos como valores faltantes y los imputamos con la mediana dentro del pipeline.
4. En la demostración de data leakage ajustamos el orden de las transformaciones para que la comparación entre el flujo correcto y el flujo con fuga fuera representativa.
5. Los hiperparámetros de `GridSearchCV` los referenciamos con el prefijo del paso correspondiente del pipeline, por ejemplo `clf__C`.
6. El modelo se guarda en `app/model.joblib`, que es la misma ruta que usa `api.py`.
7. La API recibe los datos como un objeto estructurado, el modelo `Paciente` de Pydantic, con los nombres de columna del dataset.
8. El despliegue en Kubernetes usa la imagen construida localmente (`imagePullPolicy: Never`), cargada con `minikube image load`.
9. Añadimos la carpeta `tests/` con una prueba de la API, que usa el workflow de integración continua.
10. Usamos la versión actual de la librería Evidently (`evidently.Report`, `evidently.presets.DataDriftPreset`), porque su forma de uso cambió respecto a versiones anteriores.
