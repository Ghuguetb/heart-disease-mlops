# Pipeline final y evaluación del modelo

Con los cinco modelos ya comparados, armamos el pipeline definitivo para el modelo que mejor resultado dio, la Regresión Logística. El pipeline incluye el preprocesamiento de las variables numéricas, que se imputan con la mediana y se escalan, y de las variables categóricas, que se codifican con OneHotEncoder. Todo esto queda dentro de un único objeto de scikit-learn, lo que evita errores y hace que el modelo sea fácil de guardar y reutilizar después.

Usamos GridSearchCV con validación cruzada de 5 folds para encontrar el mejor valor del hiperparámetro `C`. El mejor resultado se obtuvo con `C=1`.

## Resultados sobre el conjunto de prueba

Evaluamos el modelo final sobre un conjunto de prueba independiente, con 184 pacientes que el modelo nunca había visto durante el entrenamiento.

- AUC de 0.931
- Accuracy de 0.864
- Sensibilidad de 85.0%
- Especificidad de 88.3%

La matriz de confusión muestra cómo se distribuyen los aciertos y los errores entre pacientes sanos y enfermos.

![Matriz de confusión](images/confusion_matrix.png)

Y la curva ROC muestra qué tan bien separa el modelo las dos clases en distintos umbrales de decisión.

![Curva ROC](images/roc_curve.png)

Al final de este notebook exportamos el modelo entrenado a `app/model.joblib`, que es el archivo que después usa la API para hacer predicciones. El notebook completo está en `notebooks/2_model_pipeline_cv.ipynb`.
