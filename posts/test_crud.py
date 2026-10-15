from io import BytesIO
from pathlib import Path
from tempfile import TemporaryDirectory

from PIL import Image
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.urls import reverse

from .models import Post


def imagen_de_prueba(nombre='ejemplo.png', color='navy'):
    archivo = BytesIO()
    Image.new('RGB', (40, 30), color).save(archivo, format='PNG')
    return SimpleUploadedFile(nombre, archivo.getvalue(), content_type='image/png')


class CrudConImagenesTests(TestCase):
    def setUp(self):
        self.media = TemporaryDirectory(prefix='blog-prueba-')
        self.addCleanup(self.media.cleanup)
        self.ajustes = override_settings(MEDIA_ROOT=self.media.name)
        self.ajustes.enable()
        self.addCleanup(self.ajustes.disable)
        self.datos = {
            'titulo': 'Publicación ficticia',
            'contenido': 'Contenido de prueba para el curso.',
            'autor': 'Autor ficticio',
            'estado': Post.Estado.PUBLICADO,
        }

    def crear(self, **cambios):
        return Post.objects.create(**(self.datos | cambios))

    def test_creacion_guarda_imagen_y_la_muestra_en_listado_y_detalle(self):
        respuesta = self.client.post(reverse('posts:crear'), {
            **self.datos, 'imagen': imagen_de_prueba(),
        })
        post = Post.objects.get()
        self.assertRedirects(respuesta, reverse('posts:detalle', args=[post.pk]))
        self.assertTrue(Path(post.imagen.path).is_file())
        with Image.open(post.imagen.path) as imagen:
            self.assertEqual(imagen.size, (40, 30))
        self.assertContains(self.client.get('/'), post.imagen.url)
        detalle = self.client.get(reverse('posts:detalle', args=[post.pk]))
        self.assertContains(detalle, post.imagen.url)
        self.assertContains(detalle, 'Publicado')
        self.assertContains(detalle, self.datos['autor'])

    def test_creacion_sin_imagen_y_detalle_funcionan(self):
        respuesta = self.client.post(reverse('posts:crear'), self.datos)
        post = Post.objects.get()
        self.assertFalse(post.imagen)
        self.assertRedirects(respuesta, reverse('posts:detalle', args=[post.pk]))
        self.assertContains(self.client.get('/'), post.titulo)

    def test_edicion_actualiza_texto_y_reemplaza_imagen(self):
        post = self.crear(imagen=imagen_de_prueba())
        imagen_anterior = post.imagen.name
        respuesta = self.client.post(reverse('posts:editar', args=[post.pk]), {
            **self.datos, 'titulo': 'Título editado',
            'imagen': imagen_de_prueba('reemplazo.png', 'green'),
        })
        post.refresh_from_db()
        self.assertEqual(post.titulo, 'Título editado')
        self.assertNotEqual(post.imagen.name, imagen_anterior)
        self.assertTrue(Path(post.imagen.path).is_file())
        self.assertRedirects(respuesta, reverse('posts:detalle', args=[post.pk]))

    def test_edicion_permite_quitar_imagen_opcional(self):
        post = self.crear(imagen=imagen_de_prueba())
        self.client.post(reverse('posts:editar', args=[post.pk]), {
            **self.datos, 'imagen-clear': 'on',
        })
        post.refresh_from_db()
        self.assertFalse(post.imagen)
        self.assertContains(self.client.get(reverse('posts:detalle', args=[post.pk])), post.titulo)

    def test_archivo_no_imagen_se_rechaza_sin_guardar(self):
        respuesta = self.client.post(reverse('posts:crear'), {
            **self.datos,
            'imagen': SimpleUploadedFile('falsa.png', b'no es una imagen', content_type='image/png'),
        })
        self.assertEqual(respuesta.status_code, 200)
        self.assertIn('imagen', respuesta.context['form'].errors)
        self.assertEqual(Post.objects.count(), 0)

    def test_campos_obligatorios_se_validan_sin_guardar(self):
        respuesta = self.client.post(reverse('posts:crear'), {'titulo': ''})
        self.assertEqual(respuesta.status_code, 200)
        self.assertIn('titulo', respuesta.context['form'].errors)
        self.assertEqual(Post.objects.count(), 0)

    def test_borrar_requiere_confirmacion_y_post(self):
        post = self.crear()
        url = reverse('posts:eliminar', args=[post.pk])
        confirmacion = self.client.get(url)
        self.assertContains(confirmacion, post.titulo)
        self.assertTrue(Post.objects.filter(pk=post.pk).exists())
        respuesta = self.client.post(url)
        self.assertRedirects(respuesta, reverse('posts:inicio'))
        self.assertFalse(Post.objects.filter(pk=post.pk).exists())

    def test_formularios_y_rutas_inexistentes(self):
        formulario = self.client.get(reverse('posts:crear'))
        self.assertContains(formulario, 'enctype="multipart/form-data"')
        self.assertContains(formulario, 'csrfmiddlewaretoken')
        self.assertEqual(list(formulario.context['form'].fields),
                         ['titulo', 'contenido', 'autor', 'estado', 'imagen'])
        for ruta in ['detalle', 'editar', 'eliminar']:
            with self.subTest(ruta=ruta):
                self.assertEqual(self.client.get(reverse(f'posts:{ruta}', args=[9999])).status_code, 404)
