from django.db import models
from django.conf import settings

class Post(models.Model):
    class Estado(models.TextChoices):
        BORRADOR = 'borrador', 'Borrador'
        PUBLICADO = 'publicado', 'Publicado'
        ARCHIVADO = 'archivado', 'Archivado'

    titulo = models.CharField(max_length=180)
    contenido = models.TextField()
    autor = models.CharField(max_length=150)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=12, choices=Estado.choices, default=Estado.BORRADOR)

    imagen = models.ImageField(upload_to='posts/', null=True, blank=True)

    propietario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='publicaciones')

    class Meta:
        ordering = ['-fecha_creacion', '-pk']

    def __str__(self):
        return self.titulo

class Perfil(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='perfil')
    biografia = models.TextField(blank=True)
    link_web = models.URLField(blank=True)
    avatar = models.ImageField(upload_to='avatares/', null=True, blank=True)

    def __str__(self):
        return f'Perfil de {self.user.username}'

# El checklist llama Profile al mismo concepto; alias sin crear otra tabla.
Profile = Perfil
