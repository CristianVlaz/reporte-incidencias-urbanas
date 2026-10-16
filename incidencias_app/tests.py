from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from .models import Categoria, Estado, Incidencia, HistorialEstado

class PaginasTests(TestCase):
    def test_inicio(self):
        self.assertEqual(self.client.get('/').status_code, 200)

    def test_acerca(self):
        self.assertEqual(self.client.get('/acerca/').status_code, 200)

class APITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.categoria = Categoria.objects.create(nombre='Baches')
        self.pendiente = Estado.objects.create(nombre='Pendiente')
        self.resuelta = Estado.objects.create(nombre='Resuelta', es_final=True)
        self.datos = {
            'titulo':'Bache en avenida principal',
            'descripcion':'Hundimiento frente a la plaza',
            'direccion':'Av. Central 100', 'comuna':'Temuco',
            'categoria':self.categoria.pk, 'estado':self.pendiente.pk,
            'prioridad':'alta', 'nombre_reportante':'Ciudadano de prueba',
            'correo_reportante':'persona@example.com',
        }

    def test_crud_completo_incidencias_y_historial(self):
        respuesta = self.client.post('/api/incidencias/', self.datos, format='json')
        self.assertEqual(respuesta.status_code, 201, respuesta.data)
        pk = respuesta.data['id']
        self.assertEqual(HistorialEstado.objects.filter(incidencia_id=pk).count(), 1)
        self.assertEqual(self.client.get('/api/incidencias/').status_code, 200)
        self.assertEqual(self.client.get(f'/api/incidencias/{pk}/').status_code, 200)
        modificados = dict(self.datos, titulo='Nueva descripción', estado=self.resuelta.pk)
        self.assertEqual(self.client.put(f'/api/incidencias/{pk}/', modificados, format='json').status_code, 200)
        self.assertEqual(HistorialEstado.objects.filter(incidencia_id=pk).count(), 2)
        self.assertEqual(self.client.patch(f'/api/incidencias/{pk}/', {'prioridad':'critica'}, format='json').status_code, 200)
        self.assertEqual(self.client.delete(f'/api/incidencias/{pk}/').status_code, 204)
        self.assertFalse(Incidencia.objects.filter(pk=pk).exists())

    def test_crud_categorias_y_estados(self):
        for url, data in [('/api/categorias/', {'nombre':'Basura'}), ('/api/estados/', {'nombre':'En proceso'})]:
            respuesta = self.client.post(url, data, format='json')
            self.assertEqual(respuesta.status_code, 201)
            pk = respuesta.data['id']
            self.assertEqual(self.client.get(url).status_code, 200)
            self.assertEqual(self.client.get(f'{url}{pk}/').status_code, 200)
            self.assertEqual(self.client.put(f'{url}{pk}/', data, format='json').status_code, 200)
            self.assertEqual(self.client.patch(f'{url}{pk}/', {'descripcion':'Probando PATCH'}, format='json').status_code, 200)
            self.assertEqual(self.client.delete(f'{url}{pk}/').status_code, 204)

    def test_historial_solo_lectura(self):
        self.assertEqual(self.client.get('/api/historial-estados/').status_code, 200)
        self.assertEqual(self.client.post('/api/historial-estados/', {}, format='json').status_code, 405)
