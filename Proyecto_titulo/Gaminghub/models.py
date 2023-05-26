from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class RolUsuario(models.Model):
    id_rol = models.BigAutoField(primary_key=True)
    nombre_rol = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre_rol

class PerfilUsuario(models.Model):
    id_perfil = models.BigAutoField(primary_key=True)
    fecha_nacimiento = models.DateField(null = True, blank = True)
    edad = models.IntegerField()
    genero = models.CharField(max_length=20)
    descripcion = models.CharField(max_length = 200)
    avatar = models.ImageField()
    id_usuario = models.ForeignKey(User, on_delete=models.CASCADE,)

   

class Publicacion(models.Model):
    id_publicacion = models.BigAutoField(primary_key=True)
    titulo = models.CharField(max_length=60)
    contenido = models.CharField(max_length = 200)
    multimedia = models.ImageField()
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

class Amistad(models.Model):
    id_amistad = models.BigAutoField(primary_key=True)
    id_amigo = models.IntegerField(null=True)
    fk_id_usuario = models.ForeignKey(User, on_delete=models.CASCADE)

