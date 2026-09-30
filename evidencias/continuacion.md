# Verificación de la continuación del blog

Fecha: 30/09/2026. Preparado antes de la apertura de las entregas 8–11 y final; aún no enviado al campus.

- 12 pruebas de integración Django aprobadas (`python manage.py test posts`). Se crearon bases e imágenes temporales para probar los flujos; no se usaron cuentas externas.
- `check` sin errores y `makemigrations --check --dry-run` sin cambios pendientes. Las migraciones 0001–0003 se aplicaron en una base local nueva.
- Recorrido real en Chrome por `/admin/`: login con un administrador local de demostración y creación de tres posts. Dos publicados y uno borrador; la página principal mostró solo los publicados.
- Creación de una cuarta publicación desde el formulario público con una imagen PNG de prueba. La vista de detalle mostró la imagen y el mensaje de creación.
- CSS cargado y estilos inspeccionados en el navegador. Navegación, logout por POST y redirección anónima de `/post/nuevo/` al login comprobados.
- Las pruebas automatizadas también cubren registro, creación única del perfil, avatar, edición, borrado con confirmación, búsqueda y denegación de cambios por otro usuario.

Capturas de esta verificación: `admin-tres-posts.png`, `inicio.png`, `post-con-imagen.png`, `ruta-protegida.png`. Los datos son ejemplos académicos; no se versionan credenciales, base de datos ni archivos media.

La versión de `main` utilizada en las entregas previas permanece sin cambios. El trabajo nuevo está en la rama `continuacion-blog`, con commits separados para cada etapa. Para entregar mediante el enlace raíz, integrar esta rama cuando corresponda habilitar la siguiente entrega.
