import pytest
from django.test import Client, TestCase
from django.urls import reverse

#verificar una URL que no existe
class test_buscar_url_inexistente(TestCase):
    def setUp(self):
        self.client = Client()

    def test_template_content(self):
        response = self.client.get('/urlinexsitente/')
        assert response.status_code == 404

#buscar url existente
class test_buscar_url_existente(TestCase):
    def setUp(self):
        self.client = Client()

    def test_template_content(self):
        response = self.client.get('/login/')
        assert response.status_code == 404

# verificar carga de usuarios en pagina registro de usuario
class test_carga_registrodeusuario(TestCase):
    def setUp(self):
        self.client = Client()

    def test_template_content(self):
        response = self.client.get('/signup/')
        assert response.status_code == 200
