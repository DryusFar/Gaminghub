from django.urls import path
from .views import login, perfil, admin1, chat, menu_principal, register, completar_perfil# Se importa la vista de urls

urlpatterns = [
    path('', login, name='login'),
    path('register', register, name='register'),
    path('perfil/', perfil, name='perfil'),
    path('admin1/', admin1, name='admin1'),
    path('chat/', chat, name='chat'),
    path('menu_principal/', menu_principal, name='menu_principal'),
    path('completar_perfil/', completar_perfil, name='completar_perfil'),
    
]
