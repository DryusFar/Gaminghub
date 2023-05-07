from django.urls import path
from .views import login, perfil,index,register,admin1, chat, menu_principal,form_publicacion # Se importa la vista de urls

urlpatterns = [
    path('login', login, name='login'),
    path('register', register, name='register'),
    path('perfil/', perfil, name='perfil'),
    path('admin1/', admin1, name='admin1'),
    path('chat/', chat, name='chat'),
    path('menu_principal/', menu_principal, name='menu_principal'),
    path('', index, name='index'),
    path('form_publicacion/', form_publicacion, name='form_publicacion'),
]
