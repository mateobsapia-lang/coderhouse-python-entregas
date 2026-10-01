# Blog Project — Python, Mateo Sapia

Evolución de un blog desde scripts de consola hasta un sitio Django con HTML y CSS. La preentrega 8 continúa el proyecto Django de la preentrega 7 en la raíz; las etapas anteriores quedan preservadas en `preentregas/` dentro del mismo repositorio.

## Ejecutar el sitio Django

Requisitos: Python 3.12 y Git.

```sh
git clone https://github.com/mateobsapia-lang/coderhouse-python-entregas.git
cd coderhouse-python-entregas
python -m venv .venv
```

Activar en Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Activar en macOS/Linux:

```sh
source .venv/bin/activate
```

Instalar y ejecutar:

```sh
python -m pip install -r requirements.txt
python manage.py check
python manage.py migrate
python manage.py runserver
```

Abrir http://127.0.0.1:8000/ para ver el inicio del blog. El menú permite visitar http://127.0.0.1:8000/acerca/ y volver al inicio. Detener con Ctrl+C.

Proyecto: `blog_project`. App principal: `posts`, registrada como `posts.apps.PostsConfig`. Idioma `es-ar`; zona `America/Argentina/Buenos_Aires`. Esta entrega agrega dos vistas basadas en funciones con `render()`, templates con herencia y CSS. No incluye todavía modelos propios ni formularios.

La configuración es de desarrollo local (`DEBUG=True`). La clave de firma se genera en memoria para cada arranque; puede fijarse con la variable de entorno `DJANGO_SECRET_KEY` para conservar sesiones entre reinicios. No contiene una clave privada persistente en el repositorio. `.gitignore` excluye `.venv/`, `venv/`, `db.sqlite3`, `.env`, temporales y cachés.

## Entregas anteriores

| Etapa | Carpeta | Ejecutar desde esa carpeta |
|---|---|---|
| 1. Entorno y evidencia | [01_entorno](preentregas/01_entorno) | `python evidencia_post.py` |
| 2. Colecciones | [02_estructuras](preentregas/02_estructuras) | `python estructura_blog.py` |
| 3. Menú interactivo | [03_interactivo](preentregas/03_interactivo) | `python sistema_blog.py` |
| 4. Funciones y validación | [04_funciones](preentregas/04_funciones) | `python sistema_blog_modular.py` |
| 5. Paquetes y módulos | [05_paquetes](preentregas/05_paquetes) | `python main.py` |
| 6. Objetos y JSON | [06_poo_json](preentregas/06_poo_json) | `python main.py` |

Las etapas 1–6 usan la biblioteca estándar. Los contenidos de los posts son datos de muestra. La evidencia de ejecución y el informe de pruebas están en `evidencias/`. Para repetir las verificaciones: `python pruebas/verificar.py` desde la raíz, con el entorno activado.

## Preentrega 8: templates y CSS

- `blog_project/urls.py` conecta las rutas de `posts` mediante `include()`.
- `posts/urls.py` define Inicio (`/`) y Acerca de (`/acerca/`).
- `posts/views.py` renderiza los templates de cada página.
- `posts/templates/posts/base.html` contiene el menú, `{% load static %}` y el bloque `content`; `inicio.html` y `acerca.html` lo extienden.
- `posts/static/posts/css/estilos.css` define los colores, la tipografía, el menú y los estilos adaptables a pantallas pequeñas.

La rama `main` contiene esta etapa. El commit `55090f8` registra la implementación de templates y CSS; la rama `continuacion-blog` preserva los avances de los módulos posteriores.

Verificación: `python manage.py check` no informa problemas. Las rutas `/`, `/acerca/` y `/static/posts/css/estilos.css` responden con código 200 al ejecutar el servidor de desarrollo.
