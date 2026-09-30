import shutil
import tempfile
from io import BytesIO
from PIL import Image
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase, override_settings
from django.urls import reverse
from .models import Perfil, Post


class BlogFlowTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.autor = get_user_model().objects.create_user('autor_demo', password='Solo-Pruebas-2026!')
        cls.otro = get_user_model().objects.create_user('otro_demo', password='Solo-Pruebas-2026!')
        cls.publicado = Post.objects.create(titulo='Python visible', contenido='Django y pruebas', autor='Autor demo', estado='publicado', propietario=cls.autor)
        cls.borrador = Post.objects.create(titulo='Borrador privado', contenido='En revisión', autor='Autor demo', propietario=cls.autor)

    def setUp(self):
        self.media = tempfile.mkdtemp(prefix='blog-test-')
        self.settings_override = override_settings(MEDIA_ROOT=self.media)
        self.settings_override.enable()
        self.addCleanup(self.settings_override.disable)
        self.addCleanup(shutil.rmtree, self.media)

    def png(self):
        buffer = BytesIO()
        Image.new('RGB', (20, 20), '#15629d').save(buffer, format='PNG')
        return SimpleUploadedFile('prueba.png', buffer.getvalue(), content_type='image/png')

    def datos(self, **extra):
        return dict(titulo='Una publicación', contenido='Contenido de prueba.', autor='Autor demo', estado='publicado', **extra)

    def test_anonymous_sees_only_published_and_no_image_is_safe(self):
        response = self.client.get(reverse('posts:inicio'))
        self.assertContains(response, 'Python visible')
        self.assertNotContains(response, 'Borrador privado')
        self.assertContains(self.client.get(reverse('posts:detalle', args=[self.publicado.pk])), 'Django y pruebas')
        self.assertEqual(self.client.get(reverse('posts:detalle', args=[self.borrador.pk])).status_code, 404)

    def test_every_write_route_redirects_anonymous(self):
        urls=[reverse('posts:crear'), reverse('posts:editar', args=[self.publicado.pk]), reverse('posts:eliminar', args=[self.publicado.pk]), reverse('posts:perfil'), reverse('posts:mis_posts')]
        for url in urls:
            for method in ('get','post'):
                with self.subTest(url=url, method=method):
                    response=getattr(self.client,method)(url)
                    self.assertEqual(response.status_code,302)
                    self.assertTrue(response.url.startswith(reverse('posts:login')))

    def test_registration_creates_exactly_one_profile_and_logs_in(self):
        response=self.client.post(reverse('posts:registro'), {'username':'nuevo_demo','first_name':'Demo','password1':'Test-Demo-73951!','password2':'Test-Demo-73951!'})
        self.assertRedirects(response, reverse('posts:perfil'))
        user=get_user_model().objects.get(username='nuevo_demo')
        self.assertEqual(Perfil.objects.filter(user=user).count(),1)
        self.assertEqual(int(self.client.session['_auth_user_id']), user.pk)

    def test_signal_also_creates_profile_outside_registration(self):
        self.assertEqual(Perfil.objects.filter(user=self.autor).count(),1)

    def test_login_and_post_logout(self):
        response=self.client.post(reverse('posts:login'),{'username':'autor_demo','password':'Solo-Pruebas-2026!'})
        self.assertRedirects(response,reverse('posts:inicio'))
        self.assertEqual(self.client.get(reverse('posts:logout')).status_code,405)
        self.assertRedirects(self.client.post(reverse('posts:logout')),reverse('posts:inicio'))
        self.assertNotIn('_auth_user_id',self.client.session)

    def test_crud_image_edit_and_confirmed_delete(self):
        self.client.force_login(self.autor)
        response=self.client.post(reverse('posts:crear'),self.datos(imagen=self.png()))
        post=Post.objects.get(titulo='Una publicación')
        self.assertEqual(post.propietario,self.autor)
        self.assertRedirects(response,reverse('posts:detalle',args=[post.pk]))
        self.assertTrue(post.imagen.storage.exists(post.imagen.name))
        self.assertContains(self.client.get(response.url),post.imagen.url)
        data=self.datos();data['titulo']='Título editado'
        self.client.post(reverse('posts:editar',args=[post.pk]),data)
        post.refresh_from_db();self.assertEqual(post.titulo,'Título editado')
        confirm=reverse('posts:eliminar',args=[post.pk])
        self.assertContains(self.client.get(confirm),'Confirmar eliminación')
        self.assertTrue(Post.objects.filter(pk=post.pk).exists())
        self.client.post(confirm)
        self.assertFalse(Post.objects.filter(pk=post.pk).exists())

    def test_other_user_cannot_edit_delete_or_view_draft(self):
        self.client.force_login(self.otro)
        for name in ('editar','eliminar'):
            url=reverse(f'posts:{name}',args=[self.publicado.pk])
            self.assertEqual(self.client.get(url).status_code,404)
            self.assertEqual(self.client.post(url,self.datos()).status_code,404)
        self.assertEqual(self.client.get(reverse('posts:detalle',args=[self.borrador.pk])).status_code,404)
        self.assertTrue(Post.objects.filter(pk=self.publicado.pk).exists())

    def test_owner_can_view_drafts_and_personal_list(self):
        self.client.force_login(self.autor)
        self.assertContains(self.client.get(reverse('posts:detalle',args=[self.borrador.pk])),self.borrador.titulo)
        self.assertContains(self.client.get(reverse('posts:mis_posts')),self.borrador.titulo)

    def test_profile_avatar_and_invalid_link(self):
        self.client.force_login(self.autor)
        response=self.client.post(reverse('posts:perfil'),{'biografia':'Aprendiendo Django.','link_web':'https://example.com','avatar':self.png()})
        self.assertRedirects(response,reverse('posts:perfil'))
        perfil=Perfil.objects.get(user=self.autor)
        self.assertEqual(perfil.biografia,'Aprendiendo Django.')
        self.assertTrue(perfil.avatar.storage.exists(perfil.avatar.name))
        self.assertContains(self.client.get(response.url),perfil.avatar.url)
        invalid=self.client.post(reverse('posts:perfil'),{'biografia':'No guardar','link_web':'esto no es una URL'})
        self.assertEqual(invalid.status_code,200)
        perfil.refresh_from_db();self.assertEqual(perfil.biografia,'Aprendiendo Django.')

    def test_search_title_content_and_empty_results(self):
        for term in ('python','pruebas'):
            self.assertContains(self.client.get(reverse('posts:inicio'),{'q':term}),self.publicado.titulo)
        self.assertContains(self.client.get(reverse('posts:inicio'),{'q':'nada-coincide'}),'No encontramos coincidencias')

    def test_empty_form_and_invalid_image_do_not_save(self):
        self.client.force_login(self.autor)
        before=Post.objects.count()
        self.assertContains(self.client.post(reverse('posts:crear'),{}),'Este campo es obligatorio')
        invalid=SimpleUploadedFile('falsa.png',b'no es imagen',content_type='image/png')
        response=self.client.post(reverse('posts:crear'),self.datos(imagen=invalid))
        self.assertEqual(response.status_code,200)
        self.assertEqual(Post.objects.count(),before)

    def test_csrf_is_required_for_destructive_post(self):
        browser=Client(enforce_csrf_checks=True)
        browser.force_login(self.autor)
        self.assertEqual(browser.post(reverse('posts:eliminar',args=[self.publicado.pk])).status_code,403)
        self.assertTrue(Post.objects.filter(pk=self.publicado.pk).exists())
