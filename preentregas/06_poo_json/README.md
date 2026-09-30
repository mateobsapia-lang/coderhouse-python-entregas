# Blog con POO y persistencia JSON

Ejecutar `python main.py` desde esta carpeta. Python 3.12+, biblioteca estándar solamente.

Se continúa el mismo repositorio y los datos de la preentrega 5. Esa versión se conserva en `../05_paquetes` para poder comparar la refactorización.

`Autor` modela nombre, bio, especialidad y redes. `Post` compone un objeto `Autor`; valida identificador, contenido, tags y estado. `Blog` mantiene objetos Post y concentra listado, búsqueda, filtros, alta y validación. `blog/modelos.py` también convierte objetos a diccionarios y reconstruye instancias.

`blog/datos.py` carga `posts.json` al iniciar, respecto a la carpeta del programa, aunque se ejecute desde otra ruta. Maneja archivo ausente, vacío, JSON inválido, estructura incorrecta, registros incompletos e identificadores duplicados con mensajes claros. Los registros inválidos se omiten y se informan.

La opción 4 crea un post en memoria. La opción 6 guarda manualmente en JSON: serializa los objetos, escribe primero un temporal y conserva el archivo anterior como `posts.json.bak`. La opción 7 sale **sin guardar automáticamente**, evitando sobrescribir un JSON incorrecto al iniciar. Para comprobar persistencia: crear (4), guardar (6), salir (7), volver a ejecutar y listar (1).

El menú conserva listado (1), búsqueda por título (2), filtrado por tag (3), incorpora validación (5) y maneja opciones inválidas. Búsqueda y filtro ignoran mayúsculas. `main.py` coordina el Blog; `blog/menu.py` agrupa la entrada y presentación.
