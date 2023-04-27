from django.urls import path
from .views import login,index # Se importa la vista de urls

urlpatterns = [
    path('', index, name='index'),
    path('login', login, name='login')
]