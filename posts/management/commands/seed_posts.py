from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth import get_user_model
from posts.models import Post

class Command(BaseCommand):
    help = 'Cargar tres posts de demostración, sin crear credenciales.'

    def add_arguments(self, parser):
        parser.add_argument('--username', required=True)

    def handle(self, *args, **options):
        try:
            usuario = get_user_model().objects.get(username=options['username'])
        except get_user_model().DoesNotExist as exc:
            raise CommandError('Crear primero el usuario desde el registro o createsuperuser.') from exc
        ejemplos = [
            ('Del script a Django', 'Una vista recibe una petición y devuelve una respuesta. Los templates separan el contenido de su presentación.', 'publicado'),
            ('Datos que persisten', 'Un modelo describe la información. Las migraciones registran los cambios del esquema y permiten reconstruir la base.', 'publicado'),
            ('Próxima práctica', 'Borrador de una publicación para revisar antes de compartir.', 'borrador'),
        ]
        for titulo, contenido, estado in ejemplos:
            Post.objects.get_or_create(titulo=titulo, propietario=usuario, defaults={'contenido': contenido, 'estado': estado, 'autor': usuario.get_full_name() or usuario.username})
        self.stdout.write(self.style.SUCCESS('Ejemplos disponibles. Ejecutar otra vez no duplica las filas.'))
