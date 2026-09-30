from django.urls import path
from . import views

app_name = 'posts'
urlpatterns = [
    path('', views.lista_posts, name='inicio'),
    path('bienvenida/', views.inicio, name='bienvenida'),
    path('acerca/', views.acerca, name='acerca'),
    path('post/nuevo/', views.crear_post, name='crear'),
    path('post/<int:pk>/', views.detalle_post, name='detalle'),
    path('post/<int:pk>/editar/', views.editar_post, name='editar'),
    path('post/<int:pk>/eliminar/', views.eliminar_post, name='eliminar'),
]
