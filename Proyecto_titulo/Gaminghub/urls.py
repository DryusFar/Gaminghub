from django.urls import path
from .views import login, register # Se importa la vista de urls

urlpatterns = [
    path('', login, name='login'),
    path('register', register, name='register'),
   
]