# Integración continua con GitHub Actions

Para asegurarnos de que el código siga funcionando cada vez que hacemos un cambio, configuramos un workflow de integración continua con GitHub Actions. Este workflow se activa automáticamente cada vez que subimos cambios al repositorio.

El workflow hace tres cosas. Primero instala todas las dependencias del proyecto, luego revisa el estilo del código con `flake8` para detectar errores de sintaxis o malas prácticas, y por último corre las pruebas automáticas con `pytest`, que verifican que la API responda correctamente.

Esto nos da la tranquilidad de que, si algo se rompe, nos enteramos de inmediato y no cuando ya es demasiado tarde. También añadimos una prueba en `tests/test_api.py` que simula una petición al endpoint `/predict` y confirma que la respuesta tenga el formato esperado.
