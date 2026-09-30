from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'posts'
urlpatterns = [
    path('cuentas/registro/', views.registro, name='registro'),
    path('cuentas/login/', auth_views.LoginView.as_view(), name='login'),
    path('cuentas/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('cuentas/perfil/', views.perfil, name='perfil'),
    path('mis-publicaciones/', views.mis_posts, name='mis_posts'),
    path('', views.lista_posts, name='inicio'),
    path('bienvenida/', views.inicio, name='bienvenida'),
    path('acerca/', views.acerca, name='acerca'),
    path('post/nuevo/', views.crear_post, name='crear'),
    path('post/<int:pk>/', views.detalle_post, name='detalle'),
    path('post/<int:pk>/editar/', views.editar_post, name='editar'),
    path('post/<int:pk>/eliminar/', views.eliminar_post, name='eliminar'),
]
