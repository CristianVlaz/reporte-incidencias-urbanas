from django.urls import path
from . import views

app_name = 'incidencias_app'

urlpatterns = [
    path('', views.home, name='home'),
    path('acerca/', views.acerca, name='acerca'),
]
