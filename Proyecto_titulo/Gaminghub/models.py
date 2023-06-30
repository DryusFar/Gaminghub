from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

# Create your models here.


class RolUsuario(models.Model):
    id_rol = models.BigAutoField(primary_key=True)
    nombre_rol = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre_rol

class PerfilUsuario(models.Model):
    id_perfil = models.BigAutoField(primary_key=True)
    fecha_nacimiento = models.DateField(null = True, blank = True)
    edad = models.IntegerField(null = True)
    genero = models.CharField(max_length=20,null = True)
    descripcion = models.CharField(max_length = 200,null = True)
    avatar = models.ImageField()
    id_usuario = models.ForeignKey(User, on_delete=models.CASCADE,)

   

class Publicacion(models.Model):
    id_publicacion = models.BigAutoField(primary_key=True)
    titulo = models.CharField(max_length=60)
    contenido = models.CharField(max_length = 200)
    multimedia = models.FileField(upload_to='multimedia/')
    #Para poner videos y fotos .FileField
    fecha_creacion = models.DateField()
    like = models.ManyToManyField(User, blank=True, related_name='like')
    dislike = models.ManyToManyField(User,blank=True, related_name='dislike')
    id_usuario = models.ForeignKey(User, on_delete=models.CASCADE,)

    def __str__(self):
        return self.titulo
 
class Comentario(models.Model):
    id_comentario = models.BigAutoField(primary_key=True)
    descripcion = models.TextField(max_length=200)
    fecha_creacion = models.DateField(null=True, auto_now_add=True)
    fk_id_usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    fk_id_publicacion = models.ForeignKey(Publicacion, on_delete=models.CASCADE)

class Grupo(models.Model):
    id_grupo = models.BigAutoField(primary_key=True)
    titulo = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=300)
    multimedia = models.ImageField(max_length=200, default='static/img/Logo.png')
    privacidad = models.IntegerField()
    fk_id_usuario = models.ForeignKey(User, on_delete=models.CASCADE)

class Sala(models.Model):
    id_sala = models.BigAutoField(primary_key=True)
    nombre_sala = models.CharField(max_length=200)
    fk_id_grupo = models.ForeignKey(Grupo, on_delete=models.CASCADE)

class Miembro(models.Model):
    id_miembro = models.BigAutoField(primary_key=True)
    fk_id_grupo = models.ForeignKey(Grupo, on_delete=models.CASCADE)#Grupo 
    fk_id_usuario = models.ForeignKey(User, on_delete=models.CASCADE)#Usuario

class RegistroGrupo(models.Model):
    id_registro = models.BigAutoField(primary_key=True)
    fk_id_grupo = models.ForeignKey(Grupo, on_delete=models.CASCADE)#Grupo 
    fk_id_usuario = models.ForeignKey(User, on_delete=models.CASCADE)#Usuario

class Notificacion(models.Model):
    id_notificacion = models.BigAutoField(primary_key=True)
    info = models.TextField(max_length = 300, null = True)
    fecha_creacion = models.DateField(null=True, auto_now_add=True)
    tipo = models.IntegerField(null=True)
    fk_id_usuario = models.ForeignKey(User, related_name='notificaciones_enviador', on_delete=models.CASCADE)
    fk_recibidor = models.ForeignKey(User, related_name='notificaciones_recibidor', on_delete=models.CASCADE, null = True)

class Solicitud(models.Model):
    id_solicitud = models.BigAutoField(primary_key=True)
    recibidor = models.IntegerField(null=True)##El usuario que esta iniciado en la pagina
    fk_id_usuario = models.ForeignKey(User, on_delete=models.CASCADE)##Enviador

class Amistad(models.Model):
    id_amistad = models.BigAutoField(primary_key=True)
    persona = models.IntegerField(null=True)##persona1
    amigo = models.IntegerField(null=True)##persona2


class Mensaje(models.Model):
    id_mensaje = models.BigAutoField(primary_key=True)
    remitente = models.ForeignKey(User, on_delete=models.CASCADE , related_name='mensajes_enviados')
    destinatario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mensajes_recibidos')
    contenido = models.TextField(null=True)
    multimedia = models.FileField(upload_to='multimedia/', null = True)
    estado = models.IntegerField(null = True)
    fecha_envio = models.DateTimeField(auto_now_add=True)

class MensajeGrupo(models.Model):
    id_mensajeGrupo = models.BigAutoField(primary_key=True)
    remitente = models.ForeignKey(User, on_delete=models.CASCADE)
    contenido = models.CharField(null=True, max_length = 400)
    multimedia = models.FileField(upload_to='multimedia/', null = True)
    fecha_envio = models.DateTimeField(auto_now_add=True)
    fk_id_sala = models.ForeignKey(Sala, on_delete=models.CASCADE)

class Titulo(models.Model):
    id_titulo = models.BigAutoField(primary_key=True)
    nombre_titulo = models.CharField(null=True, max_length=100)


class Puntaje(models.Model):
    id_puntaje = models.BigAutoField(primary_key=True)
    puntos = models.IntegerField(null=True)
    fk_id_titulo = models.ForeignKey(Titulo, on_delete=models.CASCADE)
    fk_id_usuario = models.ForeignKey(User, on_delete=models.CASCADE)

