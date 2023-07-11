from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect , JsonResponse
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.views import View
from .models import Comentario, RolUsuario,PerfilUsuario,Publicacion,Grupo,Miembro,Solicitud, Amistad, Notificacion, Mensaje, Titulo, Puntaje, RegistroGrupo,Sala,MensajeGrupo
from django.db.models import Q , Case, When
from django.contrib import messages
import datetime
from PIL import Image
from django.conf import settings
import os
from urllib.parse import urlencode
from django.http import Http404
from django.core.files import File


##Import models cuando esten listos##

from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .forms import CustomUserCreationForm
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required, user_passes_test




# Create your views here.

def is_superuser(user):
    return user.is_superuser


#INICIAR SESIÓN
@user_passes_test(lambda u: not u.is_authenticated, login_url='index')
def loginView(request):
    if request.method == 'GET':
        return render(request, 'loginView.html')
    else:
        username = request.POST['username']
        password = request.POST['password']
        
        # Check if user is banned before authenticating
        try:
            user = User.objects.get(username=username)
            if user.is_active == False:
                error = 'El usuario que ingreso se encuentra baneado'
                return render(request, 'loginView.html', {'error': error})
        except User.DoesNotExist:
            user = None
        
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_superuser:
            login(request, user)
            return redirect('admin1')
        elif user is not None:
            login(request, user)
            return redirect('index')
        else:
            error = 'Usuario y/o contraseña incorrecto'
            return render(request, 'loginView.html', {'error': error})



@login_required
def perfil(request):
    if request.user.is_authenticated:
        username_id = request.user.id
    else:
        username_id = None

    user = User.objects.get(id=username_id)
    listadopublicaciones = Publicacion.objects.all().filter(id_usuario_id = user)
    puntaje = Puntaje.objects.get(fk_id_usuario = user)

    chat = Mensaje.objects.filter((Q(destinatario = username_id) & Q(estado=1)))

    try:
        perfil = PerfilUsuario.objects.get(id_usuario = username_id)
    except PerfilUsuario.DoesNotExist:
        perfil = None  # O utiliza un valor por defecto si lo deseas

    context = {
        'username': user,
        'perfil': perfil,
        'listados':listadopublicaciones,
        'titulo':puntaje,
        'chat':chat,
    }


    return render(request, 'newperfil.html',context)
@login_required
@user_passes_test(is_superuser)
def admin1(request):

    if request.user.is_authenticated:
        username_id = request.user.id
    else:
        username_id = None

    chat = Mensaje.objects.filter((Q(destinatario = username_id) & Q(estado=1)))

    user = User.objects.all().filter(is_superuser = 0)
    
    context = {
        'username': user,
        'chat':chat,
    }

    return render(request, 'admin1.html',context)

@login_required
def chat2(request):
    return render(request, 'chat2.html')

@login_required
def grupos(request):
    if request.user.is_authenticated:
        username_id = request.user.id
    else:
        username_id = None

    chat = Mensaje.objects.filter((Q(destinatario = username_id) & Q(estado=1)))

    user = User.objects.get(id=username_id)
    miembros = Miembro.objects.filter(fk_id_usuario=username_id).values_list('fk_id_grupo', flat=True)
    listadogrupos = Grupo.objects.all()

    context = {
        'username': user,
        'listados': listadogrupos,
        'miembro':miembros,
        'chat': chat,
    }
    return render(request, 'grupos.html',context)

@login_required
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


    chat = Mensaje.objects.filter((Q(destinatario = username_id) & Q(estado=1)))

    try:
        perfil = PerfilUsuario.objects.get(id_usuario = username_id)
    except PerfilUsuario.DoesNotExist:
        perfil = None  # O utiliza un valor por defecto si lo deseas

    context = {
        'username': user,
        'perfil': perfil,
        'listados': listadopublicaciones,
        'listadosp': listadoperfiles,
        'chat': chat,
    }
    return render(request, 'index.html',context )


@login_required
def register(request):
        
    return render(request, 'register.html')

@login_required
def form_publicacion(request):
    if request.user.is_authenticated:
        username_id = request.user.id
    else:
        username_id = None

    chat = Mensaje.objects.filter((Q(destinatario = username_id) & Q(estado=1)))

    user = User.objects.get(id=username_id)
    try:
        perfil = PerfilUsuario.objects.get(id_usuario = username_id)
    except PerfilUsuario.DoesNotExist:
        perfil = None  # O utiliza un valor por defecto si lo deseas

    context = {
        'username': user,
        'perfil':perfil,
        'chat':chat,
    }

    return render(request, 'form_publicacion.html', context)

@login_required
def form_modificarPublicacion(request, id_publicacion):
    if request.user.is_authenticated:
        username_id = request.user.id
    else:
        username_id = None

    chat = Mensaje.objects.filter((Q(destinatario = username_id) & Q(estado=1)))

    user = User.objects.get(id=username_id)
    publicacion = Publicacion.objects.get(id_publicacion = id_publicacion)

    context = {
        'username': user,
        'publicacion':publicacion,
        'chat':chat,
    }

    return render(request, 'form_modificarPublicacion.html', context)


@login_required
def completar_perfil(request):
    if request.user.is_authenticated:
        username_id = request.user.id
    else:
        username_id = None

    chat = Mensaje.objects.filter((Q(destinatario = username_id) & Q(estado=1)))

    user = User.objects.get(id=username_id)

    try:
        perfil = PerfilUsuario.objects.get(id_usuario = username_id)
    except PerfilUsuario.DoesNotExist:
        perfil = None  # O utiliza un valor por defecto si lo deseas

    context = {
        'username': user,
        'chat':chat,
        'perfil':perfil,
    }


   
    return render(request, 'completar_perfil.html', context)

@login_required
def modificar_perfil(request):
    if request.user.is_authenticated:
        username_id = request.user.id
    else:
        username_id = None

    chat = Mensaje.objects.filter((Q(destinatario = username_id) & Q(estado=1)))

    

    user = User.objects.get(id=username_id)

    try:
        perfil = PerfilUsuario.objects.get(id_usuario = username_id)
    except PerfilUsuario.DoesNotExist:
        perfil = None  # O utiliza un valor por defecto si lo deseas

    context = {
        'username': user,
        'perfil': perfil,
        'chat': chat,
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

             # Asignar imagen por defecto al avatar del perfil del usuario
            default_avatar_path = os.path.join('static', 'img', 'Logo.png')
            perfil_usuario = PerfilUsuario.objects.create(
                id_usuario=user,
                avatar=File(open(default_avatar_path, 'rb')),

            )


            titulo = Titulo.objects.get(id_titulo = 1)

            user1 = User.objects.get(id = user.id)

            Puntaje.objects.create(puntos = 0, fk_id_titulo= titulo, fk_id_usuario = user1)

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


@login_required
def perfilC(request):

    if request.user.is_authenticated:
        username_id = request.user.id
    else:
        username_id = None

    perfil = PerfilUsuario.objects.get(id_usuario = username_id)

    user = User.objects.get(id=username_id)

    fecha_u = request.POST['fecha_nac']
    genero_u = request.POST['genero']
    edad_u = request.POST['edad']
    descripcion_u = request.POST['descripcion']
    


    if request.FILES.get('foto'):
        avatar_u = request.FILES['foto']

        perfil.fecha_nacimiento = fecha_u
        perfil.edad = edad_u
        perfil.genero = genero_u
        perfil.descripcion = descripcion_u
        perfil.avatar = avatar_u

        perfil.save()
    else:
        avatar_u = None

        perfil.fecha_nacimiento = fecha_u
        perfil.edad = edad_u
        perfil.genero = genero_u
        perfil.descripcion = descripcion_u

        perfil.save()
        
    messages.success(request,'Datos completados exitosamente')
    return redirect('perfil')

##Pagina modificarPerfil##
@login_required
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
@login_required
def registrarpublicacion(request):

    if request.user.is_authenticated:
        username_id = request.user.id
    else:
        username_id = None

    user = User.objects.get(id=username_id)

    titulo_p = request.POST['titulo']
    contenido_p = request.POST['contenido']
    fecha_p = datetime.datetime.now()

    if request.FILES.get('multimedia'):
        multimedia_p = request.FILES['multimedia']
    else:
        multimedia_p = None


    
    
    publicacion = Publicacion.objects.create(titulo = titulo_p, contenido = contenido_p, multimedia = multimedia_p ,fecha_creacion = fecha_p ,id_usuario = user)    
    publicacion.like.set([])
    publicacion.dislike.set([])
    messages.success(request,'---Publicacion creada exitosamente---')
    return redirect('index')

@login_required
def modificarPublicacion(request,id_publicacion):
    if request.user.is_authenticated:
        username_id = request.user.id
    else:
        username_id = None

    user = User.objects.get(id=username_id)

    publicacion = Publicacion.objects.get(id_publicacion = id_publicacion)

    titulo_p = request.POST['titulo']
    contenido_p = request.POST['contenido']
    ##password_u = request.POST['password']
    
    if request.FILES.get('multimedia'):
        multimedia_p = request.FILES['multimedia']
    else:
        multimedia_p = None

    if(multimedia_p == None or multimedia_p == ""):
        multimedia_p = publicacion.multimedia
    


    publicacion.titulo = titulo_p
    publicacion.contenido = contenido_p
    publicacion.multimedia = multimedia_p
    

    publicacion.save()
    messages.success(request,'Publicacion modificada exitosamente')
    return redirect('perfil')
    
def listadopublicaciones(request):
    if request.user.is_authenticated:
        username_id = request.user.id
    else:
        username_id = None

    chat = Mensaje.objects.filter((Q(destinatario = username_id) & Q(estado=1)))
    user = User.objects.get(id=username_id)

    listadop = Publicacion.objects.all()

   
    contexto = {'username': user, 
    "listados" : listadop, 'chat':chat,}

    return render(request , 'index.html',contexto)
##############publicacion##################

#####Admin°°°°°°°°°°°°°°°
@login_required
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

    chat = Mensaje.objects.filter((Q(destinatario = username_id) & Q(estado=1)))

    user = User.objects.get(id=username_id)

    password_u = request.POST['password1']

    # Comprobar si las contraseñas coinciden

    user.password = password_u
    
    user.save()

    context = {
        'username': user,
        'perfil': perfil,
        'chat':chat
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

@login_required
def form_grupo(request):
    if request.user.is_authenticated:
        username_id = request.user.id
    else:
        username_id = None

    chat = Mensaje.objects.filter((Q(destinatario = username_id) & Q(estado=1)))

    context = {
        'chat':chat
    }
    return render(request, 'form_grupo.html', context)

@login_required
def form_modificarGrupo(request, id_grupo):
    grupo = Grupo.objects.get(id_grupo = id_grupo)
    context ={
        "grupo":grupo

    }
    return render(request, 'form_modificarGrupo.html', context)

@login_required
def registrargrupo(request):

    if request.user.is_authenticated:
        username_id = request.user.id
    else:
        username_id = None

    user = User.objects.get(id=username_id)

    titulo_g = request.POST['titulo']
    descripcion_g = request.POST['contenido']
    privacidad_g = request.POST['privacidad_g']

    if request.FILES.get('multimedia'):
        multimedia_g = request.FILES['multimedia']
    else:
        multimedia_g = None

    

    Grupo.objects.create(titulo = titulo_g, descripcion = descripcion_g, multimedia = multimedia_g , fk_id_usuario = user, privacidad = privacidad_g)    
    return redirect('grupos')

@login_required
def registrargrupo(request):

    if request.user.is_authenticated:
        username_id = request.user.id
    else:
        username_id = None

    user = User.objects.get(id=username_id)

    titulo_g = request.POST['titulo']
    descripcion_g = request.POST['contenido']
    privacidad_g = request.POST['privacidad_g']

    if request.FILES.get('multimedia'):
        multimedia_g = request.FILES['multimedia']
    else:
        multimedia_g = None

    

    Grupo.objects.create(titulo = titulo_g, descripcion = descripcion_g, multimedia = multimedia_g , fk_id_usuario = user, privacidad = privacidad_g)    
    return redirect('grupos')

@login_required
def unirse_grupo(request,id_grupo):

    if request.user.is_authenticated:
        username_id = request.user.id
    else:
        username_id = None

    user = User.objects.get(id=username_id)
    grupo = Grupo.objects.get(id_grupo = id_grupo)
    puntaje = Puntaje.objects.get(fk_id_usuario = user)
    Miembro.objects.create(fk_id_usuario = user, fk_id_grupo = grupo)   

    try:
        registro = RegistroGrupo.objects.get(fk_id_grupo=grupo, fk_id_usuario=user)
    except RegistroGrupo.DoesNotExist:
        registro = None

    if registro is not None:
        puntaje_antiguo = puntaje.puntos
        puntaje_final = puntaje.puntos

    else:
        puntaje_antiguo = puntaje.puntos
        puntaje.puntos += 1000
        puntaje.save()
        RegistroGrupo.objects.create(fk_id_usuario = user, fk_id_grupo = grupo) 
        puntaje_final = puntaje.puntos

    cambiar_titulo(puntaje, puntaje_antiguo, puntaje_final)

    return redirect('grupos')

def cambiar_titulo(puntaje, puntaje_antiguo, puntaje_final):
    user = User.objects.get(id = puntaje.fk_id_usuario.id)
    
    ###Se verifica si se hubo algun cambio con el puntaje del usuario###
    if(puntaje_antiguo != puntaje_final):
        if(puntaje.puntos == 1000):
            titulo = Titulo.objects.get(id_titulo=2)
            puntaje.fk_id_titulo = titulo
            puntaje.save()
            Notificacion.objects.create(fk_recibidor=user, tipo=5, fk_id_usuario=user)
            pass

        elif(puntaje.puntos == 3000):
            titulo = Titulo.objects.get(id_titulo=3)
            puntaje.fk_id_titulo = titulo
            puntaje.save()
            Notificacion.objects.create(fk_recibidor=user, tipo=5, fk_id_usuario=user)
            pass

        elif(puntaje.puntos == 6000):
            titulo = Titulo.objects.get(id_titulo=4)
            puntaje.fk_id_titulo = titulo
            puntaje.save()
            Notificacion.objects.create(fk_recibidor=user, tipo=5, fk_id_usuario=user)
            pass
        else:
            pass
    else:
        pass
    

@login_required
def salir_grupo(request, id_grupo):
    if request.user.is_authenticated:
        username_id = request.user.id
    else:
        username_id = None

    user = User.objects.get(id=username_id)
    grupo = Grupo.objects.get(id_grupo=id_grupo)
    miembro = Miembro.objects.filter(fk_id_grupo=grupo, fk_id_usuario=user).first()

    if miembro is not None:  # Verificar si el objeto miembro existe
        miembro.delete()
    else:
        messages.error(request, 'No eres miembro de este grupo.')

    return redirect('grupos')

@login_required
def eliminar_grupo(request, id_grupo):
    if request.user.is_authenticated:
        username_id = request.user.id
    else:
        username_id = None

    user = User.objects.get(id=username_id)
    grupo = Grupo.objects.get(id_grupo=id_grupo)

    if grupo is not None:  # Verificar si el objeto miembro existe
        grupo.delete()
    else:
        messages.error(request, 'El grupo no existe de este grupo.')

    return redirect('grupos')

def eliminar_sala(request, sala_id):
    if request.user.is_authenticated:
        username_id = request.user.id
    else:
        username_id = None

    user = User.objects.get(id=username_id)
    sala = Sala.objects.get(id_sala=sala_id)

    grupo = Grupo.objects.get(id_grupo = sala.fk_id_grupo.id_grupo)

    if sala is not None:  # Verificar si el objeto miembro existe
        sala.delete()
        messages.success(request, 'Se ha eliminado la sala exitosamente...')
    else:
        messages.error(request, 'La sala no existe en este grupo.')

    return redirect('salas', grupo_id = grupo.id_grupo)

def perfiles(request, username):
    usuario = get_object_or_404(User, username=username) #OBTENGO TODOS LOS MODELOS DE User COMPLETOS COMPARANDO EL USERNAME CON EL INGRESADO EN LA URL
    perfil_usuario = PerfilUsuario.objects.get(id_usuario=usuario) #OBTENGO EL MODELO PERFILUSUARIO CON SU FK QUE COINCIDA CON EL USUARIO OBTENIDO ANTERIORMENTE
    publicaciones = Publicacion.objects.filter(id_usuario=usuario)  # Utiliza filter en lugar de get si esperas múltiples publicaciones

    if request.user.is_authenticated:
        username_id = request.user.id
    else:
        username_id = None

    chat = Mensaje.objects.filter((Q(destinatario = username_id) & Q(estado=1)))

    notificacion_pendiente = Notificacion.objects.filter(
    Q(fk_id_usuario=request.user, fk_recibidor=perfil_usuario.id_usuario) |
    Q(fk_id_usuario=perfil_usuario.id_usuario, fk_recibidor=request.user),
    tipo=1
    ).exists()

    # Consulta para obtener la cantidad de amigos
    cantidad_amigos = Amistad.objects.filter(persona=perfil_usuario.id_usuario.id).count()
    


    if username_id == usuario.id:
        return redirect('perfil')
    else:
        return render(request, 'perfiles.html',{'user':username_id, 'usuario': usuario, 'avatar_url': perfil_usuario.avatar.url, 'publicaciones' : publicaciones,'notificacion_pendiente':notificacion_pendiente, 'chat':chat, 'cantidad_amigos':cantidad_amigos})

    

def buscar_usuarios(request):
    if request.method == 'GET' and 'term' in request.GET:
        term = request.GET.get('term')
        usuarios = User.objects.filter(username__icontains=term)[:5]
        resultados = [{'id': usuario.id, 'username': usuario.username} for usuario in usuarios]
        return JsonResponse(resultados, safe=False)
    else:
        return JsonResponse([], safe=False)

########################## LIKE Y DISLIKE ########################
class Darlikes(View):
    def post(self,request, id_publicacion,*args,**kwargs):
        post = Publicacion.objects.get(id_publicacion=id_publicacion)

        is_dislike = False
        for dislike in post.dislike.all():
            if dislike == request.user:
                is_dislike = True
                break
        
        if is_dislike:
            post.dislike.remove(request.user)


        is_like = False
        for likes in post.like.all():
            if likes == request.user:
                is_like = True
                break
        
        if not is_like:
            post.like.add(request.user)
        
        if is_like:
            post.like.remove(request.user)

        # Obtener la URL actual de la página
        next = request.META.get('HTTP_REFERER', '/')

        anchor = 'likes'  # Cambia esto al nombre del ancla deseado
        params = urlencode({'#': anchor})
        next_url = f'{next}?{params}'

        return HttpResponseRedirect(next_url)

class Dardislikes(View):
    def post(self,request, id_publicacion,*args,**kwargs):

        post = Publicacion.objects.get(id_publicacion=id_publicacion)

        is_like = False
        for likes in post.like.all():
            if likes == request.user:
                is_like = True
                break
        
        if is_like:
            post.like.remove(request.user)
        
        
        is_dislike = False
        for dislike in post.dislike.all():
            if dislike == request.user:
                is_dislike = True
                break

        if not is_dislike:
            post.dislike.add(request.user)

        if is_dislike:
            post.dislike.remove(request.user)
        
        next = request.POST.get('next','/')
        return HttpResponseRedirect(next)       
     
#######################################################

def eliminar_publicacion(request,id_publicacion):

    if request.user.is_authenticated:
        username_id = request.user.id
    else:
        username_id = None

    user = User.objects.get(id=username_id)

    publicacion = Publicacion.objects.get(id_publicacion = id_publicacion)

    publicacion.delete()
    messages.success(request,'Publicacion eliminada exitosamente...')
    return redirect('perfil')

def eliminar_publicacion_perfiles(request,id_publicacion,id_username):

    if request.user.is_authenticated:
        username_id = request.user.id
    else:
        username_id = None

    usuario = get_object_or_404(User, username=id_username)
    perfil_usuario = PerfilUsuario.objects.get(id_usuario=usuario) #OBTENGO EL MODELO PERFILUSUARIO CON SU FK QUE COINCIDA CON EL USUARIO OBTENIDO ANTERIORMENTE
    publicaciones = Publicacion.objects.filter(id_usuario=usuario)  # Utiliza filter en lugar de get si esperas múltiples publicaciones

    publicacion = Publicacion.objects.get(id_publicacion = id_publicacion)

    publicacion.delete()
    messages.success(request,'Publicacion eliminada exitosamente...')

    notificacion_pendiente = Notificacion.objects.filter(
    Q(fk_id_usuario=request.user, fk_recibidor=perfil_usuario.id_usuario) |
    Q(fk_id_usuario=perfil_usuario.id_usuario, fk_recibidor=request.user),
    tipo=1
    ).exists()



    return redirect('perfiles', username = id_username)


@login_required
def modificargrupo(request,id_grupo):

    if request.user.is_authenticated:
        username_id = request.user.id
    else:
        username_id = None

    user = User.objects.get(id=username_id)
    grupo = Grupo.objects.get(id_grupo = id_grupo)

    titulo_g = request.POST['titulo']
    descripcion_g = request.POST['descripcion']
    privacidad_g = request.POST['privacidad_g']

    if request.FILES.get('multimedia'):
        multimedia_g = request.FILES['multimedia']
    else:
        multimedia_g = None

    if(multimedia_g == None or multimedia_g == ""):
        multimedia_g = grupo.multimedia

    grupo.titulo = titulo_g
    grupo.descripcion = descripcion_g
    grupo.privacidad = privacidad_g
    grupo.multimedia = multimedia_g

    grupo.save()
    messages.success(request,'Grupo Modificado exitosamente')
    return redirect('grupos')



#Ver miembros de los grupos
def vista_miembros(request, grupo_id):
    grupo = Grupo.objects.get(id_grupo=grupo_id) #Obtengo el grupo correspondiente comparando la idGrupo de la url
    creador = grupo.fk_id_usuario #Obtengo el creador del grupo ( fk_id_usuario corresponde a la relacion con el Usuario creador)
    miembros = Miembro.objects.filter(fk_id_grupo=grupo) # Obtengo los miembros filtrando (fk_id_grupo corresponde a la realacion de los miembros conel grupo correspondiente)
    cantidad_miembros = miembros.count()  # Obtiene la cantidad de miembros
    
    return render(request, 'vista_miembros.html', {
        'grupo': grupo, 
        'creador': creador, 
        'miembros': miembros, 
        'cantidad_miembros': cantidad_miembros,
        })

########################## COMENTARIOS ########################

@login_required
def registrarcomentario(request, id_publicacion):
    if request.method == 'POST':
        descripcion_c = request.POST.get('descripcion')
        user = request.user
        publicacion = Publicacion.objects.get(id_publicacion=id_publicacion)
        Comentario.objects.create(descripcion=descripcion_c, fk_id_usuario=user, fk_id_publicacion=publicacion)

        return redirect('comentarios', id_publicacion=id_publicacion)
    
    

    if request.user.is_authenticated:
        username_id = request.user.id
    else:
            username_id = None

    chat = Mensaje.objects.filter((Q(destinatario = username_id) & Q(estado=1)))

    user = User.objects.get(id=username_id)


    user = request.user
    publicacion = Publicacion.objects.get(id_publicacion=id_publicacion)
    listadoc = Comentario.objects.filter(fk_id_publicacion=id_publicacion)

    context = {
        'username': user,
        'publicacion': publicacion,
        'listados': listadoc,
        'chat':chat
    }
            
    return render(request, 'comentarios.html', context)

def comentarios(request,id_publicacion):
    if request.user.is_authenticated:
        username_id = request.user.id
    else:
        username_id = None
    
    user = User.objects.get(id=username_id)
    publicacion_id = Publicacion.objects.get(id_publicacion = id_publicacion)
    listadoc = Comentario.objects.filter(fk_id_publicacion=id_publicacion)


    context = {
        'username': user,
        'publicacion':publicacion_id,
        'listados': listadoc,
    }
    return render(request , 'comentarios.html',context)

def eliminar_comentario(request, id_comentario):
    if request.user.is_authenticated:
        username_id = request.user.id
    else:
        username_id = None

    user = User.objects.get(id=username_id)
    comentario_eliminar = Comentario.objects.get(id_comentario=id_comentario)
    publicacion = comentario_eliminar.fk_id_publicacion
    comentario_eliminar.delete()

    messages.success(request, 'Comentario eliminado exitosamente...')
    return redirect('comentarios', id_publicacion=publicacion.id_publicacion)

###SolicitudAmistad###

def solicitudAmistad(request, id_amigo):

    if request.user.is_authenticated:
        username_id = request.user.id
    else:
        username_id = None

    user = User.objects.get(id=username_id)  

    amigo = User.objects.get(id=id_amigo)  

    

    Solicitud.objects.create(recibidor = id_amigo, fk_id_usuario = user)  
    Notificacion.objects.create(fk_recibidor = amigo, tipo = 1, fk_id_usuario = user)


    return redirect('perfiles', username=amigo.username)

def notificaciones(request):
    if request.user.is_authenticated:
        username_id = request.user.id
    else:
        username_id = None

    chat = Mensaje.objects.filter((Q(destinatario = username_id) & Q(estado=1)))

    user = User.objects.get(id=username_id)  

    listadonotificaciones = Notificacion.objects.all().filter(fk_recibidor = user).order_by('tipo')

    context = {
        'username': user,
        'listados': listadonotificaciones,
        'chat': chat
    }

    return render(request, 'notificaciones.html', context)

def agregarAmigo(request,id_notifi, id_enviador):
    
    if request.user.is_authenticated:
        username_id = request.user.id
    else:
        username_id = None

    user = User.objects.get(id=username_id)  

    amigo = User.objects.get(id = id_enviador)

    Amistad.objects.create(persona = user.id, amigo = amigo.id)
    Amistad.objects.create(persona = amigo.id, amigo = user.id)

    solicitud = Solicitud.objects.get(recibidor=user.id, fk_id_usuario=id_enviador)
    
    solicitud.delete()

    notificacion = Notificacion.objects.get(id_notificacion = id_notifi)

    notificacion.delete()

    Notificacion.objects.create(fk_recibidor = amigo, tipo = 2, fk_id_usuario = user)

    return redirect ('notificaciones')

def declinarSolicitud(request,id_notifi, id_enviador):

    if request.user.is_authenticated:
        username_id = request.user.id
    else:
        username_id = None

    user = User.objects.get(id=username_id)  

    amigo = User.objects.get(id = id_enviador)

    solicitud = Solicitud.objects.get(recibidor=user.id, fk_id_usuario=id_enviador)
    
    solicitud.delete()

    notificacion = Notificacion.objects.get(id_notificacion = id_notifi)

    notificacion.delete()

    Notificacion.objects.create(fk_recibidor = amigo, tipo = 3, fk_id_usuario = user)

    return redirect ('notificaciones')

def botonOK(request,id_notifi):

    notificacion = Notificacion.objects.get(id_notificacion = id_notifi)

    notificacion.delete()

    return redirect('notificaciones')


def amigos(request):
    # Obtener el usuario actual
    usuario_actual = request.user

    if request.user.is_authenticated:
        username_id = request.user.id
    else:
        username_id = None

    user = User.objects.get(id = usuario_actual.id)

    chat = Mensaje.objects.filter((Q(destinatario = username_id) & Q(estado=1)))

    # Obtener todas las amistades del usuario actual
    amistades = Amistad.objects.filter(persona=usuario_actual.id)

    # Crear una lista para almacenar los amigos
    amigos = []

    # Recorrer las amistades y obtener los amigos
    for amistad in amistades:
        amigo_id = amistad.amigo
        # Obtener el nombre de usuario del amigo utilizando el ID
        amigo = User.objects.get(id=amigo_id)
        # Obtener el perfil del amigo utilizando la relación id_usuario en PerfilUsuario
        amigo_perfil = PerfilUsuario.objects.get(id_usuario=amigo_id)
        # Agregar el amigo y su avatar a la lista
        mensaje_amigo = Mensaje.objects.filter(remitente = amigo_id , destinatario = usuario_actual.id, estado = 1)
        amigos.append({
            'username': amigo.username,
            'id_u' : amigo.id,
            'avatar': amigo_perfil.avatar.url if amigo_perfil else None,
            'mensaje': mensaje_amigo
        })

    # Puedes pasar la lista de amigos al contexto de renderización
    return render(request, 'amigos.html', {'amigos': amigos, 'chat':chat, 'user':user})

def eliminarAmigo(request, id_enviador):

    usuario_actual = request.user
    
    eliminar1 = Amistad.objects.get(persona = id_enviador, amigo = usuario_actual.id)
    eliminar2 = Amistad.objects.get(persona = usuario_actual.id, amigo = id_enviador)

    eliminar1.delete()
    eliminar2.delete()

    return redirect('amigos')

def chat(request, amigo_id):
    # Obtener el usuario actual
    usuario_actual = request.user

    # Obtener el amigo utilizando el ID recibido
    amigo = User.objects.get(id=amigo_id)

    # Verificar si son amigos
    son_amigos = Amistad.objects.filter(
        (Q(persona=usuario_actual.id) & Q(amigo=amigo.id)) |
        (Q(persona=amigo.id) & Q(amigo=usuario_actual.id))
    ).exists()

    if not son_amigos:
        return redirect('index')


    # Obtener el perfil del amigo
    perfil_amigo = PerfilUsuario.objects.get(id_usuario=amigo)

    # Obtener los mensajes entre el usuario actual y el amigo
    mensajes = Mensaje.objects.filter(
        (Q(remitente=usuario_actual) & Q(destinatario=amigo)) |
        (Q(remitente=amigo) & Q(destinatario=usuario_actual))
    ).order_by('fecha_envio')

    mensajes2 = Mensaje.objects.filter(Q(remitente=amigo) & Q(destinatario=usuario_actual))

    for mensaje in mensajes2:
        mensaje.estado = 2
        mensaje.save()

    return render(request, 'chat.html', {'amigo': amigo, 'mensajes': mensajes, 'perfil_amigo': perfil_amigo})

def enviarMensaje(request, amigo_id):
    if request.method == 'POST':
        # Obtener el usuario actual
        usuario_actual = request.user

        # Obtener el amigo utilizando el ID recibido
        amigo = User.objects.get(id=amigo_id)

        # Obtener el contenido del mensaje desde el formulario
        contenido = request.POST.get('mensaje')

        if request.FILES.get('multimedia'):
            archivo = request.FILES['multimedia']
        else:
            archivo = None

        if archivo:
            mensaje = Mensaje.objects.create(remitente=usuario_actual, destinatario=amigo,multimedia=archivo, contenido=contenido, estado = 1)
        else:
            # Crear un nuevo objeto de Mensaje
            mensaje = Mensaje.objects.create(remitente=usuario_actual, destinatario=amigo, contenido=contenido, estado = 1)

        # Redireccionar a la vista de chat con el amigo
        return redirect('chat', amigo_id=amigo_id)

    # Si no se envió un formulario POST, puedes manejarlo según tus necesidades
    # Por ejemplo, mostrar un error o redireccionar a otra página

    # Agrega un retorno de respuesta adecuado aquí
    return HttpResponse("Solo se permite enviar mensajes a través de POST")

def error_404(request, exception):
    return render(request, '404.html', status=404)

def crearsala(request, grupo_id):
    if request.user.is_authenticated:
        username_id = request.user.id
    else:
        username_id = None

    user = User.objects.get(id=username_id)  

    grupo = Grupo.objects.get(id_grupo = grupo_id)

    context = {
        'user':user,
        'grupo':grupo
    }

    return render(request, 'crearsala.html',context)

def salaC(request, grupo_id):

    if request.user.is_authenticated:
        username_id = request.user.id
    else:
        username_id = None

    titulo = request.POST['titulo']

    user = User.objects.get(id=username_id) 

    grupo = Grupo.objects.get(id_grupo = grupo_id) 

    Sala.objects.create(nombre_sala=titulo, fk_id_grupo = grupo)

    return redirect('salas', grupo_id=grupo.id_grupo)


def salas(request, grupo_id):
    if request.user.is_authenticated:
        username_id = request.user.id
    else:
        username_id = None

    user = User.objects.get(id=username_id)  

    grupo = Grupo.objects.get(id_grupo = grupo_id)

    
    salas = Sala.objects.filter(fk_id_grupo = grupo)
    
    context = {
        'user':user,
        'grupo':grupo,
        'salas':salas
    }

    return render(request, 'salas.html',context)

def chatSala(request, sala_id):
    if request.user.is_authenticated:
        username_id = request.user.id
    else:
        username_id = None

    user = User.objects.get(id=username_id)  

    sala = Sala.objects.get(id_sala = sala_id)

    chatSala = MensajeGrupo.objects.filter(fk_id_sala = sala)
    
    context = {
        'user':user,
        'chat':chatSala,
        'sala':sala
    }

    return render(request, 'chatSala.html',context)

def enviarMensajeGrupo(request, sala_id):
    if request.method == 'POST':
        # Obtener el usuario actual
        usuario_actual = request.user

        sala = Sala.objects.get(id_sala = sala_id)

        # Obtener el contenido del mensaje desde el formulario
        contenido = request.POST.get('mensaje')

        # Obtener el archivo adjunto desde el formulario
        if request.FILES.get('multimedia'):
            archivo = request.FILES['multimedia']
        else:
            archivo = None

        print(archivo)

        if archivo:
            MensajeGrupo.objects.create(remitente=usuario_actual, contenido=contenido, multimedia=archivo, fk_id_sala = sala)
        else:
            # Crear un nuevo objeto de Mensaje
            MensajeGrupo.objects.create(remitente=usuario_actual, contenido=contenido, fk_id_sala = sala)

        # Redireccionar a la vista de chat con el amigo
        return redirect('chatSala',sala.id_sala)

    # Si no se envió un formulario POST, puedes manejarlo según tus necesidades
    # Por ejemplo, mostrar un error o redireccionar a otra página

    # Agrega un retorno de respuesta adecuado aquí
    return HttpResponse("Solo se permite enviar mensajes a través de POST")

def enviarNotificacionMensaje(request, id_usuario):

    if request.user.is_authenticated:
        username_id = request.user.id
    else:
        username_id = None

    usuario = User.objects.get(id=id_usuario)

    chat = Mensaje.objects.filter((Q(destinatario = username_id) & Q(estado=1)))

    context = {
        'usuario':usuario,
        'chat':chat,
    }

    return render(request, 'enviarNotificacionMensaje.html', context)

def mensajeAdmin(request, id_usuario):

    usuario_actual = request.user

    usuario_recibidor = User.objects.get(id=id_usuario)

    mensaje = request.POST['mensaje']

    Notificacion.objects.create(info = mensaje, tipo = 4, fk_id_usuario = usuario_actual, fk_recibidor = usuario_recibidor)

    messages.success(request, 'Notificacion enviada')
    return redirect('admin1')

def get_messages(request, amigo_id):
     # Obtener el usuario actual
    usuario_actual = request.user

    # Obtener el amigo utilizando el ID recibido
    amigo = User.objects.get(id=amigo_id)

    # Obtener el perfil del amigo
    perfil_amigo = PerfilUsuario.objects.get(id_usuario=amigo)

    # Obtener los mensajes entre el usuario actual y el amigo
    mensajes = Mensaje.objects.filter(
        (Q(remitente=usuario_actual) & Q(destinatario=amigo)) |
        (Q(remitente=amigo) & Q(destinatario=usuario_actual))
    ).order_by('fecha_envio')

    messages_data = []  # Agrega esta línea para inicializar la lista

    for mensaje in mensajes:

        multimedia = None  # Valor por defecto si no hay archivo multimedia

    # Verificar si hay un archivo multimedia en el mensaje
        if mensaje.multimedia:
            filename, extension = os.path.splitext(mensaje.multimedia.name)

            if extension.lower() in ['.jpg', '.jpeg', '.png', '.gif']:
                multimedia = {
                    'type': 'image',
                    'url': mensaje.multimedia.url
                }
            elif extension.lower() in ['.mp4', '.avi', '.mov', '.wmv']:
                multimedia = {
                    'type': 'video',
                    'url': mensaje.multimedia.url
                }

        message_data = {
            'remitente': mensaje.remitente.username,
            'contenido': mensaje.contenido,
            'multimedia': multimedia
        }
        messages_data.append(message_data)

    return JsonResponse({'messages': messages_data})

def get_messages_grupo(request, sala_id):
    # Obtener los mensajes de la sala específica utilizando el ID recibido
    mensajes = MensajeGrupo.objects.filter(fk_id_sala=sala_id).order_by('fecha_envio')

    messages_data = []

    for mensaje in mensajes:

        multimedia = None  # Valor por defecto si no hay archivo multimedia

    # Verificar si hay un archivo multimedia en el mensaje
        if mensaje.multimedia:
            filename, extension = os.path.splitext(mensaje.multimedia.name)

            if extension.lower() in ['.jpg', '.jpeg', '.png', '.gif']:
                multimedia = {
                    'type': 'image',
                    'url': mensaje.multimedia.url
                }
            elif extension.lower() in ['.mp4', '.avi', '.mov', '.wmv']:
                multimedia = {
                    'type': 'video',
                    'url': mensaje.multimedia.url
                }
            elif extension.lower() in ['.mp3', '.wav', '.ogg']:
                multimedia = {
                    'type': 'audio',
                    'url': mensaje.multimedia.url
                }

        message_data = {
            'remitente': mensaje.remitente.username,
            'contenido': mensaje.contenido,
            'multimedia': multimedia,
        }
        messages_data.append(message_data)

    return JsonResponse({'messages': messages_data})

def form_modificarSala(request, sala_id):
    sala = Sala.objects.get(id_sala = sala_id)

    context = {
        'sala':sala,
    }

    return render(request, 'form_modificarSala.html', context)

def modificarSala(request,sala_id):
    sala = Sala.objects.get(id_sala = sala_id)

    grupo = Grupo.objects.get(id_grupo = sala.fk_id_grupo.id_grupo)

    titulo = request.POST['titulo']

    sala.nombre_sala = titulo
    sala.save()

    return redirect('salas', grupo_id = grupo.id_grupo)


def newperfil(request):
    return render(request, 'newperfil.html')