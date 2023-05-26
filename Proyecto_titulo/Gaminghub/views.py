from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect , JsonResponse
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.views import View
from .models import Comentario, RolUsuario,PerfilUsuario,Publicacion,Grupo,Miembro
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

    try:
        perfil = PerfilUsuario.objects.get(id_usuario = username_id)
    except PerfilUsuario.DoesNotExist:
        perfil = None  # O utiliza un valor por defecto si lo deseas

    context = {
        'username': user,
        'perfil': perfil,
        'listados':listadopublicaciones,
    }
    return render(request, 'perfil.html',context)

@login_required
@user_passes_test(is_superuser)
def admin1(request):

    user = User.objects.all().filter(is_superuser = 0)
    
    context = {
        'username': user,
    }

    return render(request, 'admin1.html',context)

@login_required
def chat(request):
    return render(request, 'chat.html')

@login_required
def grupos(request):
    if request.user.is_authenticated:
        username_id = request.user.id
    else:
        username_id = None

    user = User.objects.get(id=username_id)
    miembros = Miembro.objects.filter(fk_id_usuario=username_id).values_list('fk_id_grupo', flat=True)
    listadogrupos = Grupo.objects.all()

    context = {
        'username': user,
        'listados': listadogrupos,
        'miembro':miembros,
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

def comentarios(request):
    return render(request, 'comentarios.html')

@login_required
def register(request):
        
    return render(request, 'register.html')

@login_required
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

@login_required
def form_modificarPublicacion(request, id_publicacion):
    if request.user.is_authenticated:
        username_id = request.user.id
    else:
        username_id = None

    user = User.objects.get(id=username_id)
    publicacion = Publicacion.objects.get(id_publicacion = id_publicacion)

    context = {
        'username': user,
        'publicacion':publicacion,
    }

    return render(request, 'form_modificarPublicacion.html', context)


@login_required
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

@login_required
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


@login_required
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
    messages.success(request,'Datos completados exitosamente')
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
    user = User.objects.get(id=username_id)

    listadop = Publicacion.objects.all()

   
    contexto = {'username': user, 
    "listados" : listadop}

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

@login_required
def form_grupo(request):
    return render(request, 'form_grupo.html')

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
    messages.success(request,'Grupo creado exitosamente')
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
    messages.success(request,'Grupo creado exitosamente')
    return redirect('grupos')

@login_required
def unirse_grupo(request,id_grupo):

    if request.user.is_authenticated:
        username_id = request.user.id
    else:
        username_id = None

    user = User.objects.get(id=username_id)
    grupo = Grupo.objects.get(id_grupo = id_grupo)

    Miembro.objects.create(fk_id_usuario = user, fk_id_grupo = grupo)    
    messages.success(request,'Te has unido exitosamente...')
    return redirect('grupos')

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
        messages.success(request, 'Te has salido exitosamente...')
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
        messages.success(request, 'Se ha eliminado el grupo exitosamente...')
    else:
        messages.error(request, 'El grupo no existe de este grupo.')

    return redirect('grupos')

def perfiles(request, username):
    usuario = get_object_or_404(User, username=username) #OBTENGO TODOS LOS MODELOS DE User COMPLETOS COMPARANDO EL USERNAME CON EL INGRESADO EN LA URL
    perfil_usuario = PerfilUsuario.objects.get(id_usuario=usuario) #OBTENGO EL MODELO PERFILUSUARIO CON SU FK QUE COINCIDA CON EL USUARIO OBTENIDO ANTERIORMENTE
    publicaciones = Publicacion.objects.filter(id_usuario=usuario)  # Utiliza filter en lugar de get si esperas múltiples publicaciones
    return render(request, 'perfiles.html',{'usuario': usuario, 'avatar_url': perfil_usuario.avatar.url, 'publicaciones' : publicaciones})

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

        next = request.POST.get('next','/')
        return HttpResponseRedirect(next)

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
def registrarcomentario(request,id_publicacion):

    if request.user.is_authenticated:
        username_id = request.user.id
    else:
        username_id = None

    user = User.objects.get(id=username_id)
    publicacion = Publicacion.objects.get(id_publicacion=id_publicacion)
    descripcion_c = request.POST['descripcion']
    listadoc = Comentario.objects.filter(fk_id_publicacion=id_publicacion)

    context = {
        'username': user,
        'publicacion':publicacion,
        'listados': listadoc,
    }
    Comentario.objects.create(descripcion = descripcion_c,fk_id_usuario = user,fk_id_publicacion = publicacion)   

    return render(request,'comentarios.html',context)


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
