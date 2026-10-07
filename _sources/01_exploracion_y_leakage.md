# Exploración de datos y data leakage

El primer paso fue conocer los datos. Revisamos cuántos pacientes había, qué tipo de variables teníamos y si faltaban datos. Encontramos que las columnas `Cholesterol` y `RestingBP` tenían varios registros en 0, algo que no tiene sentido desde el punto de vista clínico, así que los tratamos como datos faltantes en vez de dejarlos como si fueran valores reales.

## Qué es el data leakage y por qué importa

Una de las partes centrales de este capítulo fue mostrar qué es el data leakage, o fuga de datos. Esto pasa cuando información del conjunto de prueba se filtra al proceso de entrenamiento sin darnos cuenta, por ejemplo cuando se escala o se transforma todo el dataset antes de separar los datos de entrenamiento y de prueba. El resultado es un modelo que parece funcionar muy bien, pero solo porque hizo trampa, y en la vida real ese rendimiento no se sostiene.

Para dejarlo claro, entrenamos el mismo modelo de dos formas. Primero escalando los datos antes de dividirlos, que es el error, y luego usando un pipeline que primero divide los datos y solo después escala, que es la forma correcta. La diferencia entre los dos resultados muestra por qué este orden importa tanto.

## Comparación de modelos

Una vez resuelto el tema del leakage, entrenamos y comparamos varios modelos de clasificación, todos dentro de un pipeline con GridSearchCV para buscar los mejores hiperparámetros. Probamos Regresión Logística, Random Forest, KNN, Gradient Boosting y SVC, y medimos su desempeño con AUC y Accuracy.

El notebook completo de esta etapa está en `notebooks/1_model_leakage_demo.ipynb`.
