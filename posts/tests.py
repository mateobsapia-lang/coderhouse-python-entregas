from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Post


class PublicacionesDesdeAdminTests(TestCase):
    def test_admin_guarda_posts_y_el_inicio_solo_muestra_publicados(self):
        admin = get_user_model().objects.create(
            username='admin_prueba', is_staff=True, is_superuser=True
        )
        admin.set_unusable_password()
        admin.save()
        self.client.force_login(admin)

        ejemplos = (
            ('Publicado desde admin', 'publicado'),
            ('Borrador privado de prueba', 'borrador'),
            ('Archivado de prueba', 'archivado'),
        )
        for titulo, estado in ejemplos:
            respuesta = self.client.post(reverse('admin:posts_post_add'), {
                'titulo': titulo,
                'contenido': 'Contenido sintetico cargado mediante el formulario admin.',
                'autor': 'Autor ficticio',
                'estado': estado,
                '_save': 'Guardar',
            })
            self.assertEqual(respuesta.status_code, 302)

        self.assertEqual(Post.objects.count(), 3)
        self.client.logout()
        respuesta = self.client.get('/')
        self.assertEqual(respuesta.status_code, 200)
        self.assertContains(respuesta, 'Publicado desde admin')
        self.assertContains(respuesta, 'Autor ficticio')
        self.assertNotContains(respuesta, 'Borrador privado de prueba')
        self.assertNotContains(respuesta, 'Archivado de prueba')

    def test_inicio_sin_publicaciones_muestra_un_estado_vacio(self):
        respuesta = self.client.get('/')
        self.assertEqual(respuesta.status_code, 200)
        self.assertContains(respuesta, 'Todavía no hay publicaciones.')
