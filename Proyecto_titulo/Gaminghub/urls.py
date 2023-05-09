from django.urls import path
from .views import loginView, perfil,index,register,admin1, chat, menu_principal, completar_perfil,form_publicacion,signup,signout, signin# Se importa la vista de urls

urlpatterns = [
    path('loginView', loginView, name='loginView'),
    path('register', register, name='register'),
    path('perfil/', perfil, name='perfil'),
    path('admin1/', admin1, name='admin1'),
    path('chat/', chat, name='chat'),
    path('menu_principal/', menu_principal, name='menu_principal'),
    path('', index, name='index'),
    path('completar_perfil/', completar_perfil, name='completar_perfil'),
    path('form_publicacion/', form_publicacion, name='form_publicacion'),
    path('signup/', signup, name='signup'),
    path('logout/',signout, name='signout'),
    path('signin/',signin, name='signin')
]

