# Heart Disease MLOps

Tarea 2 del curso de Machine Learning, Maestría en Ingeniería Biomédica, Universidad del Norte.

Este proyecto lo hicimos Santiago Díaz, Gina Huguet y Leiry Mares.

## De qué trata el proyecto

Las enfermedades cardiovasculares son la primera causa de muerte en el mundo, y detectarlas a tiempo marca una diferencia enorme para los pacientes. Con este proyecto quisimos ponernos en ese escenario y construir un modelo que prediga si una persona está en riesgo de sufrir una falla cardíaca, usando datos clínicos como la presión sanguínea, el colesterol o la edad.

Pero el objetivo no era solo entrenar un modelo. Lo que buscamos fue recorrer todo el camino que sigue un modelo de Machine Learning cuando se quiere llevar a producción. Eso incluye explorar los datos, evitar errores comunes como el data leakage, entrenar y comparar varios modelos, exponer el mejor modelo como una API, empaquetarla con Docker, desplegarla en Kubernetes, automatizar pruebas con integración continua y, al final, monitorear si los datos que llegan nuevos se parecen a los que usamos para entrenar.

Todo este flujo lo hicimos de forma local, sin usar servicios en la nube.

## El dataset

Usamos el [Heart Failure Prediction Dataset](https://www.kaggle.com/datasets/fedesoriano/heart-failure-prediction) de Kaggle. Tiene registros de 918 pacientes con 11 variables clínicas, como la edad, el sexo, el tipo de dolor en el pecho, la presión en reposo, el colesterol y varios resultados de electrocardiograma. La variable que queremos predecir se llama `HeartDisease` y toma el valor 1 cuando el paciente tiene riesgo de falla cardíaca y 0 cuando no.

## Cómo está organizado este libro

A continuación vas a encontrar un capítulo por cada etapa del proyecto, en el mismo orden en que las fuimos trabajando. Primero la exploración de los datos y la demostración de data leakage, luego el entrenamiento del modelo final, después el despliegue con FastAPI, Docker y Kubernetes, y por último la integración continua y el monitoreo de deriva de datos.

Este es el flujo completo, de principio a fin.

![Flujo del proyecto](images/pipeline_diagram.png)

Si quieres revisar el código directamente, el repositorio completo está en GitHub.

[github.com/Ghuguetb/heart-disease-mlops](https://github.com/Ghuguetb/heart-disease-mlops)
