from django.urls import path
from .views import Dardislikes,listadopublicaciones, loginView, perfil,index,register,admin1, chat, menu_principal, completar_perfil,form_publicacion, registrarpublicacion,signup,signout, signin,perfilC,modificar_perfil,perfilM,banearUsuario, cambiar_clave,cambiarC, perfiles ,Darlikes ,buscar_usuarios# Se importa la vista de urls

urlpatterns = [
    path('accounts/login/', loginView, name='loginView'),
    path('register', register, name='register'),
    path('perfil/', perfil, name='perfil'),
    path('admin1/', admin1, name='admin1'),
    path('chat/', chat, name='chat'),
    path('menu_principal/', menu_principal, name='menu_principal'),
    path('', index, name='index'),
    path('completar_perfil/', completar_perfil, name='completar_perfil'),
    path('modificar_perfil/', modificar_perfil, name='modificar_perfil'),
    path('cambiar_clave/', cambiar_clave, name='cambiar_clave'),
    path('form_publicacion/', form_publicacion, name='form_publicacion'),
    path('signup/', signup, name='signup'),
    path('logout/',signout, name='signout'),
    path('signin/',signin, name='signin'),


    path('perfilC/', perfilC, name='perfilC'),
    path('perfilM/',perfilM, name='perfilM'),
    path('cambiarC/',cambiarC,name='cambiarC'),

    path('banearUsuario/<id_usuario>', banearUsuario, name="banearUsuario"),

    #publicaciones
    path('registrarpublicacion/',registrarpublicacion, name='registrarpublicacion'),
    path('listadopublicaciones/', listadopublicaciones, name='listadopublicaciones'),

    path('perfiles/<str:username>/', perfiles, name='perfiles'),
    path('buscar_usuarios/', buscar_usuarios, name='buscar_usuarios'),


    #Like y Dislike
    path('post/<int:id_publicacion>/like', Darlikes.as_view(), name='like'),
    path('post/<int:id_publicacion>/dislike>', Dardislikes.as_view(), name='dislike'),
]

