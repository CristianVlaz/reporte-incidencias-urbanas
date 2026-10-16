from django.contrib import admin
from .models import Categoria, Estado, Incidencia, HistorialEstado

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'activo')
    search_fields = ('nombre',)

@admin.register(Estado)
class EstadoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'es_final')

class HistorialInline(admin.TabularInline):
    model = HistorialEstado
    extra = 0
    readonly_fields = ('estado_anterior', 'estado_nuevo', 'observacion', 'fecha_cambio')
    can_delete = False

    def has_add_permission(self, request, obj=None):
        return False

@admin.register(Incidencia)
class IncidenciaAdmin(admin.ModelAdmin):
    list_display = ('id', 'titulo', 'categoria', 'estado', 'prioridad', 'comuna', 'fecha_reporte')
    list_filter = ('categoria', 'estado', 'prioridad', 'comuna')
    search_fields = ('titulo', 'descripcion', 'direccion')
    inlines = [HistorialInline]

    def save_model(self, request, obj, form, change):
        anterior = None
        if change:
            anterior = Incidencia.objects.get(pk=obj.pk).estado_id
        super().save_model(request, obj, form, change)
        if anterior is None or anterior != obj.estado_id:
            HistorialEstado.objects.create(
                incidencia=obj,
                estado_anterior_id=anterior,
                estado_nuevo=obj.estado,
                observacion='Registro desde Django Admin',
            )

@admin.register(HistorialEstado)
class HistorialEstadoAdmin(admin.ModelAdmin):
    list_display = ('id', 'incidencia', 'estado_anterior', 'estado_nuevo', 'fecha_cambio')
    readonly_fields = ('incidencia', 'estado_anterior', 'estado_nuevo', 'observacion', 'fecha_cambio')

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False
