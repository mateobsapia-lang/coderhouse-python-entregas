# Blog Project — Python, Mateo Sapia

Evolución de un blog desde scripts de consola hasta la base de Django. El proyecto Django de la preentrega 7 está en la raíz; las etapas anteriores quedan preservadas en `preentregas/` dentro del mismo repositorio.

## Ejecutar la base Django

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

Abrir http://127.0.0.1:8000/ para ver la pantalla inicial de Django. Detener con Ctrl+C.

Proyecto: `blog_project`. App principal: `posts`, registrada como `posts.apps.PostsConfig`. Idioma `es-ar`; zona `America/Argentina/Buenos_Aires`. Esta entrega prepara únicamente la base: no incluye modelos propios, vistas ni templates del blog.

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

## Continuación: módulo 8
Inicio y Acerca de usan herencia de templates y CSS de la app. Rama `continuacion-blog`, preparada antes de la apertura del campus.

## Módulo 9: modelos y admin
Ejecutar `python manage.py migrate` y `python manage.py createsuperuser`. Ingresar a `/admin/` con ese usuario y cargar al menos tres Posts de estados diferentes. El inicio lista solo publicados, ordenados por fecha. Base local ignorada; repetir estos pasos al clonar.

## Módulo 10: CRUD e imágenes
Formularios multipart y `request.FILES` guardan imágenes en `media/posts/`. `MEDIA_ROOT` usa BASE_DIR; las URLs de desarrollo sirven los archivos. La carpeta media no se versiona: subir imágenes nuevas desde el formulario al reconstruir el proyecto. Los detalles toleran publicaciones sin imagen.

## Módulo 11: cuentas y perfil
Registro, login, logout por POST y perfil con biografía, enlace y avatar. Las acciones de escritura requieren sesión y la propiedad del post. `Perfil` es el modelo; `Profile` es un alias para el nombre usado en el checklist. Una señal crea el perfil automáticamente y el registro usa `get_or_create` para no duplicarlo.
