from django.db import models

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

    class Meta:
        ordering = ['-fecha_creacion', '-pk']

    def __str__(self):
        return self.titulo
