# Verificación realizada

Python 3.12.10. Dependencias Django instaladas en entorno virtual.

`python pruebas/verificar.py`: 8 pruebas aprobadas. Verifican estructura de datos y autor anidado; menú con opciones inválidas; búsqueda y filtro sin distinguir mayúsculas; funciones tolerantes a registros incompletos; integración de paquetes; serialización y reconstrucción de objetos; JSON ausente, vacío o incorrecto; alta, guardado, cierre y nueva ejecución con el nuevo post.

`python manage.py check`: System check identified no issues (0 silenced).

`python manage.py migrate --noinput`: migraciones estándar de admin, auth, contenttypes y sessions aplicadas correctamente. La base SQLite local está excluida de Git.

`preentregas/01_entorno/checkpoint_modulo1.txt`: salida real del script, con intérprete de entorno virtual.
