from django.urls import path
from .views import login, perfil, admin1, chat, menu_principal # Se importa la vista de urls

urlpatterns = [
    path('', login, name='login'),
    path('perfil/', perfil, name='perfil'),
    path('admin1/', admin1, name='admin1'),
    path('chat/', chat, name='chat'),
    path('menu_principal/', menu_principal, name='menu_principal')
]