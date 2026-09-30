# Bitácora Python — Mateo Sapia

Blog académico desarrollado con Python 3.12, Django 5.2, SQLite, HTML, CSS y Pillow. Continúa el mismo proyecto de los módulos anteriores. La rama `continuacion-blog` contiene las preentregas 8–11 y la consolidación final preparadas antes de su apertura; `main` conserva la versión presentada hasta el módulo 7.

## Funcionalidades

- Inicio y Acerca de con herencia de templates y CSS propio, sin CDN.
- Posts con título, contenido, autor, fecha, estado e imagen opcional.
- CRUD web; eliminación con confirmación y POST.
- Registro, login, logout por POST y perfil con biografía, web y avatar.
- Escritura protegida por `login_required`. Solo el propietario puede editar o borrar su post. Borradores y archivados solo son visibles para su propietario.
- Búsqueda de publicaciones por título o contenido; mensaje sin resultados.
- Admin con filtros por estado y búsqueda.

## Instalación local desde cero

```bash
git clone --branch continuacion-blog https://github.com/mateobsapia-lang/coderhouse-python-entregas.git
cd coderhouse-python-entregas
python -m venv .venv
```

Activar en Windows PowerShell: `.\.venv\Scripts\Activate.ps1`. En macOS/Linux: `source .venv/bin/activate`.

```bash
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Abrir http://127.0.0.1:8000/. Para el admin, abrir `/admin/` y usar el superusuario creado localmente. No hay usuarios ni contraseñas reales incluidos en el repositorio.

### Datos y archivos de demostración

La base SQLite y `media/` no se versionan. `migrate` reconstruye el esquema. Desde `/admin/`, agregar al menos tres posts con distintos estados para repetir la práctica del módulo 9. También se puede usar `python manage.py seed_posts --username TU_USUARIO` para cargar tres ejemplos sintéticos sin crear credenciales. Repetir el comando no duplica los ejemplos existentes del usuario.

Crear publicaciones desde «Escribir» o `/post/nuevo/`, elegir una imagen PNG/JPEG y guardar. `ImageField` y Pillow validan el archivo. `enctype="multipart/form-data"` y `request.FILES` permiten cargarlo en `media/posts/`. Los avatares van a `media/avatares/`. Los templates comprueban si hay imagen antes de acceder a su URL. En desarrollo, las URLs de media se sirven con DEBUG; no es una configuración de despliegue público.

### Variables de entorno

La app lee variables del proceso. `.env.example` es una guía; no carga automáticamente un archivo `.env` ni requiere python-decouple. Sin `DJANGO_SECRET_KEY`, genera un secreto temporal al arrancar, por lo que las sesiones dejan de valer al reiniciar. Para conservar sesiones, exportar una clave local aleatoria estable antes de iniciar el servidor. Nunca subirla a Git.

Ejemplo PowerShell:
```powershell
$env:DJANGO_SECRET_KEY = python -c "import secrets; print(secrets.token_urlsafe(50))"
$env:DJANGO_DEBUG = "true"
python manage.py runserver
```

El proyecto usa `BASE_DIR`; no contiene rutas absolutas. DEBUG y servidor de desarrollo se destinan a práctica local.

## Pruebas

```bash
python manage.py check
python manage.py makemigrations --check --dry-run
python manage.py test posts
python pruebas/verificar.py
```

Las pruebas del blog usan una base temporal y archivos de imágenes temporales. Cubren registro, perfil, login/logout, CRUD, imágenes, rutas anónimas, permisos entre usuarios, borradores, búsqueda, validaciones y CSRF. Los resultados de la verificación están en `evidencias/continuacion.md`.

## Recorrido y archivos

- `preentregas/01_entorno` a `06_poo_json`: ejercicios iniciales ya presentados.
- `blog_project/`: configuración y URLs del proyecto, iniciado en módulo 7.
- Módulo 8: `posts/templates/posts/{base,inicio,acerca}.html` y `posts/static/posts/css/estilos.css`.
- Módulo 9: modelo Post, admin, migración 0001 y lista desde el ORM. Commit: **Checkpoint: Modelos y Admin configurados**.
- Módulo 10: ModelForm, imagen, migración 0002 y CRUD.
- Módulo 11: usuarios, `Perfil`, signals, migración 0003 y permisos.
- Final: integración, búsqueda, documentación y verificaciones.

La consigna usa los nombres `Profile` y `Perfil`: se implementó el modelo `Perfil` con alias `Profile`, sin duplicar tablas. `post_save` crea el perfil y la vista de registro llama a `get_or_create`, conciliando la señal pedida por el checklist con la creación explícita de la actividad. `autor` es una firma de presentación; `propietario` identifica la cuenta autorizada para modificar el post.

Autor: **Mateo Sapia**. Proyecto académico para el curso de Python de Coderhouse. Datos de demostración ficticios.
