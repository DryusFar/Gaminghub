from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def login(request):
    return render(request,'login.html')

def perfil(request):
    return render(request,'perfil.html')

def admin1(request):
    return render(request,'admin1.html')

def chat(request):
    return render(request,'chat.html')

def menu_principal(request):
    return render(request,'menu_principal.html')
