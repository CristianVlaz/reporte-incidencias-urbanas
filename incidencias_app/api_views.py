from django.db import transaction
from rest_framework import viewsets
from rest_framework.exceptions import MethodNotAllowed
from .models import Categoria, Estado, Incidencia, HistorialEstado
from .serializers import (
    CategoriaSerializer, EstadoSerializer, IncidenciaSerializer, HistorialEstadoSerializer,
)

class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer

class EstadoViewSet(viewsets.ModelViewSet):
    queryset = Estado.objects.all()
    serializer_class = EstadoSerializer

class IncidenciaViewSet(viewsets.ModelViewSet):
    queryset = Incidencia.objects.select_related('categoria', 'estado').all()
    serializer_class = IncidenciaSerializer

    @transaction.atomic
    def perform_create(self, serializer):
        incidencia = serializer.save()
        HistorialEstado.objects.create(
            incidencia=incidencia, estado_nuevo=incidencia.estado,
            observacion='Estado inicial de la incidencia',
        )

    @transaction.atomic
    def perform_update(self, serializer):
        actual = self.get_object()
        estado_anterior_id = actual.estado_id
        incidencia = serializer.save()
        if estado_anterior_id != incidencia.estado_id:
            HistorialEstado.objects.create(
                incidencia=incidencia,
                estado_anterior_id=estado_anterior_id,
                estado_nuevo=incidencia.estado,
                observacion='Cambio registrado mediante API REST',
            )

class HistorialEstadoViewSet(viewsets.ReadOnlyModelViewSet):
    """Historial auditable: GET permitido; no se pueden falsificar cambios por API."""
    queryset = HistorialEstado.objects.select_related('incidencia', 'estado_anterior', 'estado_nuevo').all()
    serializer_class = HistorialEstadoSerializer
