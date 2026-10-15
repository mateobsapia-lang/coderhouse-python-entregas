# Verificación de la preentrega 10

15 de octubre de 2026. Python 3.12.10, Django 5.2.17 y Pillow 12.3.0, ejecutados desde el entorno virtual local del proyecto.

- `python manage.py check`: sin problemas.
- `python manage.py makemigrations --check --dry-run`: no faltan migraciones.
- `python manage.py migrate --noinput`: `posts.0002_post_imagen` aplicada correctamente.
- `python manage.py test posts --verbosity 2`: **10 pruebas aprobadas**. Incluyen las dos verificaciones de la etapa 9 y ocho del CRUD: creación con/sin imagen, detalle y listado, edición y reemplazo, quitar la imagen opcional, rechazo de archivos inválidos, campos obligatorios, confirmación y borrado por POST, formularios multipart y rutas inexistentes.
- `python pruebas/verificar.py`: **8 pruebas de consola aprobadas**.

Se probó además la interfaz real en Chrome, con el servidor de desarrollo escuchando únicamente en `127.0.0.1:8765`: creación desde `/post/nuevo/` con un PNG ficticio de 800 × 360 píxeles, redirección al detalle e imagen cargada con sus dimensiones correctas; edición del título y reemplazo del archivo, con una nueva URL media comprobada; entrada a la confirmación de borrado y eliminación por el botón correspondiente, seguida de redirección al listado vacío. El contenido de prueba se eliminó desde la propia interfaz al terminar.

La base SQLite, las imágenes de usuario y el entorno virtual están ignorados por Git. Esta etapa es de desarrollo local y no incorpora las funcionalidades de autenticación del módulo 11.
