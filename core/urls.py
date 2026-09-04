"""
Configuración de URLs del proyecto core.

Las rutas propias de la aplicación viven en incidencias_app/urls.py.
Aquí solo se registra el panel de administración y se "incluye" el
urlconf de la aplicación, tal como indica la documentación de Django:
https://docs.djangoproject.com/en/stable/topics/http/urls/
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('incidencias_app.urls')),
]
