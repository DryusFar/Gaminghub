from django.shortcuts import render, redirect
from django.http import HttpResponse
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import RolUsuario,PerfilUsuario,Publicacion
from django.contrib import messages
import datetime
from PIL import Image
from django.conf import settings
import os
##Import models cuando esten listos##

from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError

# Create your views here.


def loginView(request):
    return render(request, 'loginView.html')


def perfil(request):
    if request.user.is_authenticated:
        username_id = request.user.id
    else:
        username_id = None

    user = User.objects.get(id=username_id)
    try:
        perfil = PerfilUsuario.objects.get(id_usuario = username_id)
    except PerfilUsuario.DoesNotExist:
        perfil = None  # O utiliza un valor por defecto si lo deseas

    context = {
        'username': user,
        'perfil': perfil
    }
    return render(request, 'perfil.html',context)


def admin1(request):
    return render(request, 'admin1.html')


def chat(request):
    return render(request, 'chat.html')


def menu_principal(request):
    return render(request, 'menu_principal.html')


def index(request):
    return render(request, 'index.html')


def register(request):
    return render(request, 'register.html')


def form_publicacion(request):
    return render(request, 'form_publicacion.html')


def completar_perfil(request):
    if request.user.is_authenticated:
        username_id = request.user.id
    else:
        username_id = None

    user = User.objects.get(id=username_id)

    context = {
        'username': user
    }


   
    return render(request, 'completar_perfil.html', context)

def modificar_perfil(request):
    if request.user.is_authenticated:
        username_id = request.user.id
    else:
        username_id = None

    

    user = User.objects.get(id=username_id)

    try:
        perfil = PerfilUsuario.objects.get(id_usuario = username_id)
    except PerfilUsuario.DoesNotExist:
        perfil = None  # O utiliza un valor por defecto si lo deseas

    context = {
        'username': user,
        'perfil': perfil
    }


   
    return render(request, 'modificar_perfil.html', context)


# REGISTRARSE
def signup(request):

    if request.method == 'GET':
        return render(request, 'signup.html', {
            'form': UserCreationForm
        })
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(
                    username=request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('index')
            except IntegrityError:
                return render(request, 'signup.html', {
                    'form': UserCreationForm,
                    "error": 'Usuario ya existe'
                })

        return render(request, 'signup.html', {
            'form': UserCreationForm,
            'error': 'Las contraseñas no coinciden'
        })


# CERRAR SESIÓN
def signout(request):
    logout(request)
    return redirect('signin')



# INICIAR SESIÓN
def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html', {
            'form': AuthenticationForm
        })
    else:
        user = authenticate(
            request, username=request.POST['username'], password=request.POST['password'])

        if user is None:
            return render(request, 'signin.html', {
                'form': AuthenticationForm,
                'error': 'Usuario y/o contraseña incorrecto'
            })
        else:
            login(request, user)
            return redirect('index')

#Funciones pagina web#

##Pagina completarPerfil##



def perfilC(request):

    if request.user.is_authenticated:
        username_id = request.user.id
    else:
        username_id = None

    user = User.objects.get(id=username_id)

    fecha_u = request.POST['fecha_nac']
    genero_u = request.POST['genero']
    edad_u = request.POST['edad']
    descripcion_u = request.POST['descripcion']
    


    if request.FILES.get('foto'):
        avatar_u = request.FILES['foto']
    else:
        avatar_u = None

    PerfilUsuario.objects.create(fecha_nacimiento = fecha_u,avatar = avatar_u,edad = edad_u, genero = genero_u, descripcion = descripcion_u, id_usuario = user)    
    messages.success(request,'Datos completados exitosamente')
    return redirect('perfil')

##Pagina modificarPerfil##

def perfilM(request):
    if request.user.is_authenticated:
        username_id = request.user.id
    else:
        username_id = None

    user = User.objects.get(id=username_id)

    perfil = PerfilUsuario.objects.get(id_usuario = user)

    correo_u = request.POST['correo']
    edad_u = request.POST['edad']
    ##password_u = request.POST['password']
    nombre_u = request.POST['nombre']
    apellido_u = request.POST['apellido']
    if request.FILES.get('foto'):
        avatar_u = request.FILES['foto']
    else:
        avatar_u = None

    fecha_u = request.POST['fecha_nac']

    if fecha_u:
        fecha_u = fecha_u
    else:
        fecha_u = None

    if(avatar_u == None or avatar_u == ""):
        avatar_u = perfil.avatar
    

    if(fecha_u == "" or fecha_u == None):
        fecha_u = perfil.fecha_nacimiento
    

    genero_u = request.POST['genero']
    descripcion_u = request.POST['descripcion']

    user.email = correo_u
    ##usuario.password = password_u
    user.first_name = nombre_u
    user.last_name = apellido_u
    perfil.edad = edad_u
    perfil.fecha_nacimiento = fecha_u
    perfil.genero = genero_u
    perfil.descripcion = descripcion_u
    perfil.avatar = avatar_u

    user.save()
    perfil.save()
    messages.success(request,'Datos modificados exitosamente')
    return redirect('perfil')



    


