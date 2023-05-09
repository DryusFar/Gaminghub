from django.shortcuts import render
from django.http import HttpResponse
from django.contrib import messages
import datetime
##Import models cuando esten listos##

# Create your views here.
def login(request):
    return render(request,'login.html')

def perfil(request):
    return render(request,'perfil.html')

def admin1(request):
    return render(request,'admin1.html')

def chat(request):
    return render(request,'chat.html')

def menu_principal(request):
    return render(request,'menu_principal.html')

def index(request):
    return render(request,'index.html')

def register(request):
    return render(request,'register.html')

def form_publicacion(request):
    return render(request,'form_publicacion.html')

def completar_perfil(request):
    return render(request,'completar_perfil.html')

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
    