from django import forms
from .models import Categoria, Estado, Incidencia


class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nombre', 'descripcion', 'activo']
        labels = {
            'nombre': 'Nombre de la categoría',
            'descripcion': 'Descripción',
            'activo': 'Categoría activa',
        }
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: Baches, Luminarias, Basura...',
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Describe el tipo de incidencias que agrupa esta categoría...',
                'rows': 3,
            }),
            'activo': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
            }),
        }


class EstadoForm(forms.ModelForm):
    class Meta:
        model = Estado
        fields = ['nombre', 'descripcion', 'es_final']
        labels = {
            'nombre': 'Nombre del estado',
            'descripcion': 'Descripción',
            'es_final': '¿Es estado final (cierra la incidencia)?',
        }
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: Pendiente, En proceso, Resuelta...',
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Explica cuándo corresponde aplicar este estado...',
                'rows': 3,
            }),
            'es_final': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
            }),
        }


class IncidenciaForm(forms.ModelForm):
    class Meta:
        model = Incidencia
        fields = [
            'titulo',
            'descripcion',
            'direccion',
            'comuna',
            'categoria',
            'estado',
            'prioridad',
            'nombre_reportante',
            'correo_reportante',
        ]
        labels = {
            'titulo': 'Título de la incidencia',
            'descripcion': 'Descripción detallada',
            'direccion': 'Dirección exacta o referencia',
            'comuna': 'Comuna',
            'categoria': 'Categoría',
            'estado': 'Estado actual',
            'prioridad': 'Nivel de prioridad',
            'nombre_reportante': 'Nombre del reportante',
            'correo_reportante': 'Correo electrónico de contacto',
        }
        widgets = {
            'titulo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: Luminaria apagada en esquina principal',
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Detalla el problema observado, riesgos y referencias...',
                'rows': 4,
            }),
            'direccion': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: Av. Alemania 0450',
            }),
            'comuna': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: Temuco',
            }),
            'categoria': forms.Select(attrs={
                'class': 'form-select',
            }),
            'estado': forms.Select(attrs={
                'class': 'form-select',
            }),
            'prioridad': forms.Select(attrs={
                'class': 'form-select',
            }),
            'nombre_reportante': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre completo del ciudadano o gestor',
            }),
            'correo_reportante': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'correo@ejemplo.cl',
            }),
        }