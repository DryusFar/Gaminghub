from django.urls import path
from .views import login, perfil # Se importa la vista de urls

urlpatterns = [
    path('', login, name='login'),
    path('perfil/', perfil, name='perfil')
]