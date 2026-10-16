from rest_framework.routers import DefaultRouter
from .api_views import CategoriaViewSet, EstadoViewSet, IncidenciaViewSet, HistorialEstadoViewSet

router = DefaultRouter()
router.register(r'categorias', CategoriaViewSet, basename='categoria')
router.register(r'estados', EstadoViewSet, basename='estado')
router.register(r'incidencias', IncidenciaViewSet, basename='incidencia')
router.register(r'historial-estados', HistorialEstadoViewSet, basename='historialestado')
urlpatterns = router.urls
