# Conclusiones

Este proyecto nos permitió entender que entrenar un buen modelo es solo una parte del trabajo. Lo que realmente marca la diferencia en un proyecto de Machine Learning real es todo lo que viene después, poder servirlo, empaquetarlo, desplegarlo, probarlo automáticamente y vigilar que siga funcionando bien con el tiempo.

El modelo final, una Regresión Logística, obtuvo un AUC de 0.931 y una Accuracy de 0.864 sobre datos que nunca había visto, lo cual nos pareció un resultado sólido para un problema clínico como este. Pero más allá del número, lo que más aprendimos fue el proceso completo, desde evitar el data leakage hasta dejar el modelo corriendo en Kubernetes con monitoreo activo.

Trabajar las seis etapas de principio a fin, de forma local y sin depender de servicios en la nube, nos ayudó a entender mejor cómo se conecta cada pieza del ciclo de vida de un modelo en producción.

## Entregables

- Repositorio en GitHub, con todo el código, los notebooks, la API, los manifiestos de Kubernetes y el workflow de integración continua.
- Un notebook único que reúne las tres etapas de análisis y modelado.
- Este libro, publicado en GitHub Pages, como guía de todo el proyecto.
