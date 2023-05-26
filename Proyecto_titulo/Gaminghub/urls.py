from django.urls import path
from .views import comentarios,listadopublicaciones, loginView, perfil,index,register,admin1, chat, menu_principal, completar_perfil,form_publicacion, registrarcomentario,registrarpublicacion,signup,signout, signin,perfilC,modificar_perfil,perfilM,banearUsuario, cambiar_clave,cambiarC,grupos,form_grupo, registrargrupo,unirse_grupo,salir_grupo,eliminar_grupo,form_modificarPublicacion, perfiles ,Darlikes ,buscar_usuarios,Dardislikes,modificarPublicacion,eliminar_publicacion, form_modificarGrupo,modificargrupo, vista_miembros # Se importa la vista de urls

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
    path('form_modificarPublicacion/<id_publicacion>', form_modificarPublicacion, name='form_modificarPublicacion'),
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
    path('modificarPublicacion/<id_publicacion>',modificarPublicacion,name='modificarPublicacion'),
    path('eliminar_publicacion/<id_publicacion>',eliminar_publicacion,name='eliminar_publicacion'),

    #grupos
    path('grupos/',grupos, name='grupos'),
    path('form_grupo',form_grupo, name='form_grupo'),
    path('form_modificarGrupo/<id_grupo>',form_modificarGrupo, name='form_modificarGrupo'),
    path('registrargrupo/',registrargrupo, name='registrargrupo'),
    path('unirse_grupo/<id_grupo>',unirse_grupo, name='unirse_grupo'),
    path('salir_grupo/<id_grupo>', salir_grupo, name='salir_grupo'),
    path('eliminar_grupo/<id_grupo>', eliminar_grupo, name='eliminar_grupo'),
    path('modificargrupo/<id_grupo>', modificargrupo, name='modificargrupo'),

    path('perfiles/<str:username>/', perfiles, name='perfiles'),
    path('buscar_usuarios/', buscar_usuarios, name='buscar_usuarios'),


    #Like y Dislike
    path('post/<int:id_publicacion>/like', Darlikes.as_view(), name='like'),
    path('post/<int:id_publicacion>/dislike>', Dardislikes.as_view(), name='dislike'),

    #Comentarios
    path('comentarios/<int:id_publicacion>', comentarios, name='comentarios'),
    path('registrarcomentario/<int:id_publicacion>',registrarcomentario, name='registrarcomentario'),

path('vista_miembros/<int:grupo_id>/', vista_miembros, name='vista_miembros'),
]

