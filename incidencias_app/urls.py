from django.urls import path
from . import views

app_name = 'incidencias_app'

urlpatterns = [
    # Vistas públicas e informativas
    path('', views.home, name='home'),
    path('acerca/', views.acerca, name='acerca'),

    # CRUD Incidencias
    path('incidencias/', views.IncidenciaListView.as_view(), name='incidencia_list'),
    path('incidencias/crear/', views.IncidenciaCreateView.as_view(), name='incidencia_create'),
    path('incidencias/<int:pk>/', views.IncidenciaDetailView.as_view(), name='incidencia_detail'),
    path('incidencias/<int:pk>/editar/', views.IncidenciaUpdateView.as_view(), name='incidencia_update'),
    path('incidencias/<int:pk>/eliminar/', views.IncidenciaDeleteView.as_view(), name='incidencia_delete'),

    # CRUD Categorías
    path('categorias/', views.CategoriaListView.as_view(), name='categoria_list'),
    path('categorias/crear/', views.CategoriaCreateView.as_view(), name='categoria_create'),
    path('categorias/<int:pk>/', views.CategoriaDetailView.as_view(), name='categoria_detail'),
    path('categorias/<int:pk>/editar/', views.CategoriaUpdateView.as_view(), name='categoria_update'),
    path('categorias/<int:pk>/eliminar/', views.CategoriaDeleteView.as_view(), name='categoria_delete'),

    # CRUD Estados
    path('estados/', views.EstadoListView.as_view(), name='estado_list'),
    path('estados/crear/', views.EstadoCreateView.as_view(), name='estado_create'),
    path('estados/<int:pk>/', views.EstadoDetailView.as_view(), name='estado_detail'),
    path('estados/<int:pk>/editar/', views.EstadoUpdateView.as_view(), name='estado_update'),
    path('estados/<int:pk>/eliminar/', views.EstadoDeleteView.as_view(), name='estado_delete'),

    # Historial de estados (solo lectura por integridad de auditoría)
    path('historial-estados/', views.HistorialEstadoListView.as_view(), name='historial_list'),
    path('historial-estados/<int:pk>/', views.HistorialEstadoDetailView.as_view(), name='historial_detail'),
]