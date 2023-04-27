from django.urls import path
from .views import login, perfil, register # Se importa la vista de urls

urlpatterns = [
    path('', login, name='login'),
    path('register', register, name='register'),
path('perfil/', perfil, name='perfil')
]
