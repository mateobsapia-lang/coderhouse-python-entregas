from django.urls import path
from . import views

app_name = 'posts'
urlpatterns = [path('', views.lista_posts, name='inicio'), path('bienvenida/', views.inicio, name='bienvenida'), path('acerca/', views.acerca, name='acerca')]
