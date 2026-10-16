from rest_framework import serializers
from .models import Categoria, Estado, Incidencia, HistorialEstado

class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')

class EstadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Estado
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')

class IncidenciaSerializer(serializers.ModelSerializer):
    categoria_nombre = serializers.CharField(source='categoria.nombre', read_only=True)
    estado_nombre = serializers.CharField(source='estado.nombre', read_only=True)

    class Meta:
        model = Incidencia
        fields = '__all__'
        read_only_fields = ('fecha_reporte', 'fecha_actualizacion')

class HistorialEstadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = HistorialEstado
        fields = '__all__'
        read_only_fields = ('incidencia', 'estado_anterior', 'estado_nuevo', 'observacion', 'fecha_cambio')
