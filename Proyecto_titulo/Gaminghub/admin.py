from django.contrib import admin
from .models import RolUsuario, PerfilUsuario,Publicacion
# Register your models here.
admin.site.register(RolUsuario)
admin.site.register(PerfilUsuario)
admin.site.register(Publicacion)