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
    multimedia = models.ImageField(upload_to='imagenes/')
    fecha_creacion = models.DateField()
    like = models.IntegerField()
    dislike = models.IntegerField()
    id_usuario = models.ForeignKey(User, on_delete=models.CASCADE,)

    def __str__(self):
        return self.titulo