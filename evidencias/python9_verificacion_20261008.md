# Verificacion del checkpoint 9

Fecha: 8 de octubre de 2026.

La version de `main` se actualizo con el modelo Post, su migracion, el registro en el admin y el listado mediante el ORM. Se conserva el proyecto de las entregas 7 y 8 y el commit solicitado: `Checkpoint: Modelos y Admin configurados`.

Validacion realizada sobre esta version:

- `python manage.py check`: sin problemas.
- `python manage.py makemigrations --check --dry-run`: sin cambios pendientes.
- `python manage.py test posts`: dos pruebas de integracion aprobadas. El cliente de prueba envia tres formularios al admin (Publicado, Borrador y Archivado), verifica que se guarden y comprueba que un visitante solo vea el publicado. Tambien comprueba el mensaje del listado vacio.
- `python manage.py migrate --noinput`: `posts.0001_initial` aplicada correctamente en la base local.

Las pruebas usan una base temporal y un administrador ficticio con contrasena inutilizable; no crean ni distribuyen credenciales reales. La base local no se sube a GitHub. Para entrar manualmente al admin, crear un superusuario local siguiendo el README.

El recorrido previo en Chrome por el admin y la carga manual de tres posts corresponde al 30 de septiembre, en la continuacion del mismo proyecto; no se atribuye a una nueva prueba manual del 8 de octubre. Los modulos posteriores siguen preparados en `continuacion-blog`.
