import pytest
from django.contrib.auth import get_user_model
User= get_user_model()

#Crear un nuevo usuario
@pytest.mark.django_db
def test_crear_usuario():
    user = User.objects.create_user(
            username='vicente123',
            email='vicente@gmail.com',
            password='123'
    )
    assert user.username == 'vicente123'

#Verificar error al crear usuario sin contraseña
@pytest.mark.django_db
def test_crear_usuario_nopassword():
    error = False
    try:
        user = User.objects.create_user(
                username='kevin123',
                email='vicente@gmail.com',
        )
    except:
        error = True
    assert not error

#Verificar error al crear usuario sin email
@pytest.mark.django_db
def test_crear_usuario_noemail():
    error = False
    try:
        user = User.objects.create_user(
                username='carlitos',
                password='12345',
        )
    except:
        error = True
    assert not error

#Verificar error al crear usuario sin mail ni contraseña
def test_crear_usuario_noemailypassword():
    error = False
    try:
        user = User.objects.create_user(
                username='hugo',
        )
    except:
        error = True
    assert not error 

# Crear un nuevo super usuario
@pytest.mark.django_db
def test_crear_superusuario():
    user = User.objects.create_superuser(
            username='carlos',
            email='carlos@gmail.com',
            password='123'
    )
    assert user.is_superuser

#Verificar permisos
@pytest.mark.django_db
def test_crear_usuario_staff():
    user = User.objects.create_superuser(
            username='vicente',
            email='vicente@gmail.com',
            password='123',
            is_staff=True
    )
    assert user.is_staff

#Verificar si el usuario existe
@pytest.mark.django_db
def test_usuario_existe():
    User.objects.create_user(
            username='vicente',
            email='vicente@gmail.com',
            password='123'
    )
    assert User.objects.filter(username='vicente').exists()
    
    assert User.objects.filter(username='vicente').exists()

# Verificar si existe un super usuario
@pytest.mark.django_db
def test_usuario_existe_fallido():
    # Crear un usuario de prueba en la base de datos
    User.objects.create_user(
            username='kevinho',
            email='kevinho@gmail.com',
            password='123'
    )
    # Verificar si el usuario existe en la base de datos
    assert User.objects.filter(username='kevinho').exists()
    
    # Verificar un usuario que no existe en la base de datos.
    assert not User.objects.filter(username='alexis').exists()
