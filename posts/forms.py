from django import forms
from .models import Post, Perfil
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['titulo', 'contenido', 'autor', 'estado', 'imagen']

class RegistroForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ('username', 'first_name', 'last_name')

class PerfilForm(forms.ModelForm):
    class Meta:
        model = Perfil
        fields = ('biografia', 'link_web', 'avatar')
