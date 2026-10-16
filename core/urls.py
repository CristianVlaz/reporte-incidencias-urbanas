from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('incidencias_app.api_urls')),
    path('', include('incidencias_app.urls')),
]
