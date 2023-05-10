from django.shortcuts import render, redirect
from django.http import HttpResponse
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib import messages
import datetime
##Import models cuando esten listos##

from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .forms import CustomUserCreationForm

# Create your views here.

#INICIAR SESIÓN
def loginView(request):
    if request.method == 'GET':
        return render(request, 'loginView.html')
    else:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            error = 'Usuario y/o contraseña incorrecto'
            return render(request, 'loginView.html', {'error': error})



def perfil(request):
    if request.user.is_authenticated:
        username = request.user.username
    else:
        username = None

    context = {
        'username': username
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
    return render(request, 'completar_perfil.html')


# REGISTRARSE
def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            # Crear un objeto usuario con los datos del formulario
            user = form.save(commit=False)
            
            # Obtener los campos adicionales del formulario
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            email = form.cleaned_data.get('email')
            
            # Asignar los campos adicionales al objeto usuario
            user.first_name = first_name
            user.last_name = last_name
            user.email = email

            # Guardar el objeto usuario en la base de datos
            user.save()

            # Autenticar al usuario y redirigir al usuario a la página de inicio
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            return redirect('index')
    else:
        form = CustomUserCreationForm()
    return render(request, 'signup.html', {'form': form})


# CERRAR SESIÓN
def signout(request):
    logout(request)
    return redirect('loginView')



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

"""

def PerfilC(request,usuario):

    usuario = Usuario.objects.get(id_usuario = usuario)
    perfil_u = PerfilUsuario.objects.get(fk_id_usuario = usuario)
    nombre_u = request.POST['nombre']
    apellido_u = request.POST['apellido']
    avatar_u = request.FILES['foto']
    fecha_u = request.POST['fecha_nac']
    genero_u = request.POST['genero']
    descripcion_u = request.POST['descripcion']
    fk_id_usuario = usuario

    nombre_completo = nombre_u + " " + apellido_u 

    PerfilUsuario.objects.create(nombre_completo = nombre_completo, fecha_nacimiento = fecha_u, genero = genero_u, correo = correo_u, avatar = avatar_u, descripcion = descripcion_u, Usuario_id_usuario = fk_id_usuario)    
    messages.success(request,'Datos completados exitosamente')
    return render(request,'perfil.html')

##Pagina modificarPerfil##

def PerfilM(request,usuario):
    usuario = Usuario.objects.get(id_usuario = usuario)
    perfil_u = Usuario.objects.get(fk_id_usuario = usuario)
    username = request.POST['nickName']
    correo_u = request.POST['correo']
    edad_u = request.POST['edad']
    password_u = request.POST['password']
    nombre_u = request.POST['nombre']
    apellido_u = request.POST['apellido']
    if (request.FILES.get("foto")):
        fotot = request.FILES['foto']
        usuario.avatar = fotot
    fecha_u = request.POST['fecha_nac']
    genero_u = request.POST['genero']
    descripcion_u = request.POST['descripcion']

    usuario.username = username
    usuario.email = correo_u
    usuario.edad = edad_u
    usuario.password = password_u
    perfil_u.nombre_completo = nombre_u + " " + apellido_u 
    perfil_u.fecha_nacimiento = fecha_u
    perfil_u.genero = genero_u
    perfil_u.descripcion = descripcion_u

    usuario.save()
    perfil_u.save()
    messages.success(request,'Datos modificados exitosamente')
    return render(request,'perfil.html')

    """
    


