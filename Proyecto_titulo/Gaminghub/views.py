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
from .forms import CustomUserCreationForm
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required, user_passes_test




# Create your views here.

#INICIAR SESIÓN
@user_passes_test(lambda u: not u.is_authenticated, login_url='index')
def loginView(request):
    if request.method == 'GET':
        return render(request, 'loginView.html')
    else:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:

            usuariot = User.objects.get(username = username)
            
            if usuariot.is_active == False:
               error = 'El usuario que ingreso se encuentra baneado xd'
               return render(request, 'loginView.html', {'error': error})
            else:
                login(request, user)
                return redirect('index')
        else:
            error = 'Usuario y/o contraseña incorrecto'
            return render(request, 'loginView.html', {'error': error})



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

    user = User.objects.all().filter(is_staff = 0)
    
    context = {
        'username': user,
    }

    return render(request, 'admin1.html',context)


def chat(request):
    return render(request, 'chat.html')


def menu_principal(request):
    return render(request, 'menu_principal.html')

def cambiar_clave(request):
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


   
    return render(request, 'cambiar_clave.html', context)



@login_required
def index(request):
    if request.user.is_authenticated:
        username_id = request.user.id
    else:
        username_id = None

    user = User.objects.get(id=username_id)
    listadopublicaciones = Publicacion.objects.all().order_by('fecha_creacion')

    listadoperfiles = PerfilUsuario.objects.all()

    try:
        perfil = PerfilUsuario.objects.get(id_usuario = username_id)
    except PerfilUsuario.DoesNotExist:
        perfil = None  # O utiliza un valor por defecto si lo deseas

    context = {
        'username': user,
        'perfil': perfil,
        'listados': listadopublicaciones,
        'listadosp': listadoperfiles,
    }
    return render(request, 'index.html',context)



def register(request):
        
    return render(request, 'register.html')


def form_publicacion(request):
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
        'perfil':perfil
    }

    return render(request, 'form_publicacion.html', context)



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
@user_passes_test(lambda u: not u.is_authenticated, login_url='index')
def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():


            # Obtener el nombre de usuario del formulario
            username = form.cleaned_data.get('username')

            # Comprobar si ya existe un usuario con ese nombre
            if User.objects.filter(username=username).exists():
                # Mostrar un mensaje de error
                form.add_error('username', 'Ya existe un usuario con ese nombre.')
                return render(request, 'signup.html', {'form': form})

            # Obtener los valores de las contraseñas
            password1 = form.cleaned_data.get('password1')
            password2 = form.cleaned_data.get('password2')


            # Comprobar si las contraseñas coinciden
            if password1 != password2:
                # Mostrar un mensaje de error
                form.add_error('password2', 'Las contraseñas no coinciden.')
                return render(request, 'signup.html', {'form': form})

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

##############publicacion##################
def registrarpublicacion(request):

    if request.user.is_authenticated:
        username_id = request.user.id
    else:
        username_id = None

    user = User.objects.get(id=username_id)

    titulo_p = request.POST['titulo']
    contenido_p = request.POST['contenido']
    fecha_p = datetime.datetime.now()
    like_p = 0
    dislike_p = 0

    if request.FILES.get('multimedia'):
        multimedia_p = request.FILES['multimedia']
    else:
        multimedia_p = None

    

    Publicacion.objects.create(titulo = titulo_p, contenido = contenido_p, multimedia = multimedia_p ,fecha_creacion = fecha_p,like = like_p,dislike = dislike_p ,id_usuario = user)    
    messages.success(request,'Datos completados exitosamente')
    return redirect('index')


    
def listadopublicaciones(request):
    if request.user.is_authenticated:
        username_id = request.user.id
    else:
        username_id = None
    user = User.objects.get(id=username_id)

    listadop = Publicacion.objects.all()

   
    contexto = {'username': user, 
    "listados" : listadop}

    return render(request , 'index.html',contexto)
##############publicacion##################

#####Admin°°°°°°°°°°°°°°°

def banearUsuario(request, id_usuario):
    usuariot = User.objects.get(id = id_usuario)

    if usuariot.is_active == True:
        usuariot.is_active = False
        usuariot.save()
        messages.success(request, '---Usuario baneado exitosamente---')
    elif usuariot.is_active == False:
        usuariot.is_active = True
        usuariot.save()
        messages.success(request, '---Usuario desbaneado exitosamente---')

    return redirect('admin1')
####Admin####

def csambiarC(request):
    if request.user.is_authenticated:
        username_id = request.user.id
    else:
        username_id = None

    user = User.objects.get(id=username_id)

    password_u = request.POST['password1']

    # Comprobar si las contraseñas coinciden

    user.password = password_u
    
    user.save()

    context = {
        'username': user,
        'perfil': perfil
    }

    messages.success(request,'Contraseña modificada exitosamente')
    return render(request, 'perfil.html', context)

@login_required
def cambiarC(request):
    if request.method == 'POST':
        # Obtener los datos del formulario
        old_password = request.POST.get('old_password')
        new_password1 = request.POST.get('password1')
        new_password2 = request.POST.get('password2')
        # Obtener el usuario actual
        user = request.user
        # Verificar que la contraseña actual sea correcta
        if not user.check_password(old_password):
            messages.error(request, 'La contraseña actual es incorrecta')
            return redirect('cambiar_clave')
        # Verificar la longitud de la nueva contraseña
        if len(new_password1) < 8:
            messages.error(request, 'La contraseña debe tener al menos 8 caracteres')
            return redirect('cambiar_clave')
        # Verificar que las nuevas contraseñas coincidan
        
        if new_password1 != new_password2:
            messages.error(request, 'Las nuevas contraseñas no coinciden')
            return redirect('cambiar_clave')
        # Actualizar la contraseña del usuario
        user.set_password(new_password1)
        user.save()
        messages.success(request, 'La contraseña ha sido cambiada exitosamente')
        return redirect('loginView')
    return render(request, 'loginView.html')