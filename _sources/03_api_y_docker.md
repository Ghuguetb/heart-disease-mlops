# API con FastAPI y Docker

Una vez que tuvimos el modelo entrenado y guardado, el siguiente paso fue exponerlo como una API para que cualquier aplicación pueda pedirle una predicción. Para esto usamos FastAPI, que es un framework de Python pensado justo para construir APIs de forma rápida y sencilla.

La API recibe los datos de un paciente a través del endpoint `/predict`, usando un modelo de Pydantic llamado `Paciente` que valida que lleguen todos los campos esperados. Internamente carga el pipeline guardado en `app/model.joblib` y devuelve la probabilidad de enfermedad cardíaca junto con la predicción final.

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

Esto devuelve algo como lo siguiente.

```json
{"heart_disease_probability": 0.9597, "prediction": 1}
```

## Por qué usamos Docker

Para que esta API funcione igual en cualquier computador, sin depender de qué versión de Python o de librerías tenga instaladas cada quien, la empaquetamos con Docker. El `Dockerfile` arma una imagen liviana que instala las dependencias necesarias y deja la API lista para correr con un solo comando.

```bash
docker build -t heart-api -f docker/Dockerfile .
docker run -p 8000:8000 heart-api
```

Con esto, la API queda corriendo en un contenedor, lista para que cualquier otra aplicación le haga peticiones.
