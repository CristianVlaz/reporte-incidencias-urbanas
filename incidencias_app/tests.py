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
            'titulo': 'Bache en avenida principal',
            'descripcion': 'Hundimiento frente a la plaza',
            'direccion': 'Av. Central 100',
            'comuna': 'Temuco',
            'categoria': self.categoria.pk,
            'estado': self.pendiente.pk,
            'prioridad': 'alta',
            'nombre_reportante': 'Ciudadano de prueba',
            'correo_reportante': 'persona@example.com',
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
        self.assertEqual(self.client.patch(f'/api/incidencias/{pk}/', {'prioridad': 'critica'}, format='json').status_code, 200)
        self.assertEqual(self.client.delete(f'/api/incidencias/{pk}/').status_code, 204)
        self.assertFalse(Incidencia.objects.filter(pk=pk).exists())

    def test_crud_categorias_y_estados(self):
        for url, data in [('/api/categorias/', {'nombre': 'Basura'}), ('/api/estados/', {'nombre': 'En proceso'})]:
            respuesta = self.client.post(url, data, format='json')
            self.assertEqual(respuesta.status_code, 201)
            pk = respuesta.data['id']
            self.assertEqual(self.client.get(url).status_code, 200)
            self.assertEqual(self.client.get(f'{url}{pk}/').status_code, 200)
            self.assertEqual(self.client.put(f'{url}{pk}/', data, format='json').status_code, 200)
            self.assertEqual(self.client.patch(f'{url}{pk}/', {'descripcion': 'Probando PATCH'}, format='json').status_code, 200)
            self.assertEqual(self.client.delete(f'{url}{pk}/').status_code, 204)

    def test_historial_solo_lectura(self):
        self.assertEqual(self.client.get('/api/historial-estados/').status_code, 200)
        self.assertEqual(self.client.post('/api/historial-estados/', {}, format='json').status_code, 405)


class CRUDWebCBVTests(TestCase):
    def setUp(self):
        self.categoria = Categoria.objects.create(nombre='Luminarias', descripcion='Alumbrado público')
        self.pendiente = Estado.objects.create(nombre='Pendiente')
        self.resuelta = Estado.objects.create(nombre='Resuelta', es_final=True)

    def test_crud_cbv_incidencias_y_auditoria(self):
        # CreateView
        resp = self.client.post(reverse('incidencias_app:incidencia_create'), {
            'titulo': 'Poste sin luz',
            'descripcion': 'Luminaria apagada en pasaje',
            'direccion': 'Pasaje Sur 45',
            'comuna': 'Temuco',
            'categoria': self.categoria.pk,
            'estado': self.pendiente.pk,
            'prioridad': 'alta',
            'nombre_reportante': 'Juan Pérez',
            'correo_reportante': 'juan@example.com',
        })
        self.assertEqual(resp.status_code, 302)
        incidencia = Incidencia.objects.get(titulo='Poste sin luz')
        self.assertEqual(HistorialEstado.objects.filter(incidencia=incidencia).count(), 1)

        # ListView & DetailView
        self.assertEqual(self.client.get(reverse('incidencias_app:incidencia_list')).status_code, 200)
        self.assertEqual(self.client.get(reverse('incidencias_app:incidencia_detail', args=[incidencia.pk])).status_code, 200)

        # Historial ListView & DetailView
        historial = HistorialEstado.objects.get(incidencia=incidencia)
        self.assertEqual(self.client.get(reverse('incidencias_app:historial_list')).status_code, 200)
        self.assertEqual(self.client.get(reverse('incidencias_app:historial_detail', args=[historial.pk])).status_code, 200)

        # UpdateView con cambio de estado
        resp_upd = self.client.post(reverse('incidencias_app:incidencia_update', args=[incidencia.pk]), {
            'titulo': 'Poste reparado',
            'descripcion': 'Luminaria operativa',
            'direccion': 'Pasaje Sur 45',
            'comuna': 'Temuco',
            'categoria': self.categoria.pk,
            'estado': self.resuelta.pk,
            'prioridad': 'media',
            'nombre_reportante': 'Juan Pérez',
            'correo_reportante': 'juan@example.com',
        })
        self.assertEqual(resp_upd.status_code, 302)
        self.assertEqual(HistorialEstado.objects.filter(incidencia=incidencia).count(), 2)

        # DeleteView (GET confirmación + POST eliminación)
        self.assertEqual(self.client.get(reverse('incidencias_app:incidencia_delete', args=[incidencia.pk])).status_code, 200)
        self.assertEqual(self.client.post(reverse('incidencias_app:incidencia_delete', args=[incidencia.pk])).status_code, 302)
        self.assertFalse(Incidencia.objects.filter(pk=incidencia.pk).exists())

    def test_crud_cbv_categorias_y_estados(self):
        # Categorías
        self.assertEqual(self.client.get(reverse('incidencias_app:categoria_list')).status_code, 200)
        self.assertEqual(self.client.post(reverse('incidencias_app:categoria_create'), {
            'nombre': 'Semáforos', 'descripcion': 'Fallas de señalética', 'activo': True,
        }).status_code, 302)
        cat = Categoria.objects.get(nombre='Semáforos')
        self.assertEqual(self.client.get(reverse('incidencias_app:categoria_detail', args=[cat.pk])).status_code, 200)
        self.assertEqual(self.client.post(reverse('incidencias_app:categoria_update', args=[cat.pk]), {
            'nombre': 'Semáforos Urbanos', 'descripcion': 'Actualizada', 'activo': True,
        }).status_code, 302)
        self.assertEqual(self.client.post(reverse('incidencias_app:categoria_delete', args=[cat.pk])).status_code, 302)

        # Estados
        self.assertEqual(self.client.get(reverse('incidencias_app:estado_list')).status_code, 200)
        self.assertEqual(self.client.post(reverse('incidencias_app:estado_create'), {
            'nombre': 'En revisión', 'descripcion': 'Evaluando en terreno', 'es_final': False,
        }).status_code, 302)
        est = Estado.objects.get(nombre='En revisión')
        self.assertEqual(self.client.get(reverse('incidencias_app:estado_detail', args=[est.pk])).status_code, 200)
        self.assertEqual(self.client.post(reverse('incidencias_app:estado_update', args=[est.pk]), {
            'nombre': 'En inspección', 'descripcion': 'Actualizado', 'es_final': False,
        }).status_code, 302)
        self.assertEqual(self.client.post(reverse('incidencias_app:estado_delete', args=[est.pk])).status_code, 302)