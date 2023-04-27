from django.urls import path
from .views import login # Se importa la vista de urls

urlpatterns = [
    path('', login, name='login'),
   
]