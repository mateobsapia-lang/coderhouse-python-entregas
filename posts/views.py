from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from .forms import PerfilForm, PostForm, RegistroForm
from .models import Perfil, Post

def inicio(request):
    return render(request, 'posts/inicio.html')

def acerca(request):
    return render(request, 'posts/acerca.html')

def lista_posts(request):
    posts = Post.objects.filter(estado='publicado').order_by('-fecha_creacion')
    busqueda = request.GET.get('q', '').strip()
    if busqueda:
        posts = posts.filter(Q(titulo__icontains=busqueda) | Q(contenido__icontains=busqueda))
    return render(request, 'posts/lista_posts.html', {'posts': posts, 'busqueda': busqueda})

@login_required
def mis_posts(request):
    posts = Post.objects.filter(propietario=request.user).order_by('-fecha_creacion')
    return render(request, 'posts/lista_posts.html', {'posts': posts, 'mis_publicaciones': True})

def detalle_post(request, pk):
    visibles = Q(estado='publicado')
    if request.user.is_authenticated:
        visibles |= Q(propietario=request.user)
    post = get_object_or_404(Post.objects.filter(visibles), pk=pk)
    return render(request, 'posts/post_detail.html', {'post': post})

@login_required
def crear_post(request):
    form = PostForm(request.POST if request.method == 'POST' else None, request.FILES or None, initial={'autor': request.user.get_full_name() or request.user.username})
    if request.method == 'POST' and form.is_valid():
        post = form.save(commit=False)
        post.propietario = request.user
        post.save()
        messages.success(request, 'Publicación creada.')
        return redirect('posts:detalle', pk=post.pk)
    return render(request, 'posts/post_form.html', {'form': form, 'titulo_pagina': 'Nueva publicación'})

@login_required
def editar_post(request, pk):
    post = get_object_or_404(Post, pk=pk, propietario=request.user)
    form = PostForm(request.POST if request.method == 'POST' else None, request.FILES or None, instance=post)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Cambios guardados.')
        return redirect('posts:detalle', pk=post.pk)
    return render(request, 'posts/post_form.html', {'form': form, 'titulo_pagina': 'Editar publicación'})

@login_required
def eliminar_post(request, pk):
    post = get_object_or_404(Post, pk=pk, propietario=request.user)
    if request.method == 'POST':
        post.delete()
        messages.success(request, 'Publicación eliminada.')
        return redirect('posts:mis_posts')
    return render(request, 'posts/post_confirm_delete.html', {'post': post})

def registro(request):
    if request.user.is_authenticated:
        return redirect('posts:perfil')
    form = RegistroForm(request.POST if request.method == 'POST' else None)
    if request.method == 'POST' and form.is_valid():
        with transaction.atomic():
            usuario = form.save()
            # La señal satisface el checklist; get_or_create evita duplicar el perfil.
            Perfil.objects.get_or_create(user=usuario)
        login(request, usuario)
        messages.success(request, 'Tu cuenta está lista.')
        return redirect('posts:perfil')
    return render(request, 'registration/registro.html', {'form': form})

@login_required
def perfil(request):
    perfil_usuario, _ = Perfil.objects.get_or_create(user=request.user)
    form = PerfilForm(request.POST if request.method == 'POST' else None, request.FILES or None, instance=perfil_usuario)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Perfil actualizado.')
        return redirect('posts:perfil')
    return render(request, 'posts/perfil.html', {'form': form, 'perfil': perfil_usuario})
