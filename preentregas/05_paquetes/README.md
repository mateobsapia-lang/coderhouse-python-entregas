# Blog por consola organizado en paquetes

Desde esta carpeta ejecutar `python main.py` (Python 3.12 o posterior; sin dependencias externas).

El menú permite listar, buscar por título, filtrar por tag, validar y salir. Búsquedas y filtros ignoran mayúsculas. Conserva los tres posts de etapas anteriores y un cuarto registro inválido para mostrar la validación.

* `main.py`: coordina el menú e importa el paquete.
* `blog/__init__.py`: identifica el paquete.
* `blog/datos.py`: autor anidado, estados, etiquetas y posts.
* `blog/menu.py`: captura de entrada y menú.
* `blog/operaciones.py`: listar, buscar y filtrar.
* `blog/validaciones.py`: revisa campos, tipos y reglas.

No usa JSON ni base de datos en esta etapa. Las etapas 5 y 6 se conservan en este mismo repositorio para revisar su evolución.
