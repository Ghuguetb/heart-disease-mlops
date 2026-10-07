# Monitoreo de deriva de datos

Un modelo entrenado hoy no necesariamente va a seguir funcionando bien dentro de unos meses, porque los datos del mundo real van cambiando con el tiempo. A este fenómeno se le conoce como data drift, o deriva de datos, y es algo que cualquier proyecto de MLOps debería poder detectar.

Para esta etapa usamos Evidently, una librería pensada justo para este tipo de monitoreo. Comparamos la distribución de `X_train`, que es nuestro conjunto de referencia, contra `X_test`, simulando que serían los datos que llegarían después en producción.

El reporte generado no mostró deriva significativa a nivel de todo el dataset. Solo una de las 11 columnas, `Sex`, mostró deriva de forma individual, y esto tiene una explicación sencilla, el desbalance natural que ya tenía esa variable en el dataset original.

El reporte completo, interactivo, queda guardado en `drift_report.html`, y el notebook que lo genera está en `notebooks/3_data_drift_monitoring.ipynb`.
