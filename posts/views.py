from django.shortcuts import render

def inicio(request):
    return render(request, 'posts/inicio.html')

def acerca(request):
    return render(request, 'posts/acerca.html')

from .models import Post

def lista_posts(request):
    posts = Post.objects.filter(estado='publicado').order_by('-fecha_creacion')
    return render(request, 'posts/lista_posts.html', {'posts': posts})
