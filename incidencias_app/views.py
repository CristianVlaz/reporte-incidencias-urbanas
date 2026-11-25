from django.contrib import messages
from django.db import transaction
from django.db.models import ProtectedError
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from .forms import CategoriaForm, EstadoForm, IncidenciaForm
from .models import Categoria, Estado, HistorialEstado, Incidencia


def home(request):
    """Vista pública de bienvenida del sistema."""
    contexto = {
        'nombre_proyecto': 'Sistema de Reporte de Incidencias Urbanas',
        'descripcion': (
            'Plataforma que permite a ciudadanos y gestores municipales '
            'registrar, dar seguimiento y auditar incidencias urbanas '
            '(baches, luminarias, basura, semáforos, etc.), centralizando '
            'la información histórica y facilitando la coordinación entre '
            'los distintos actores involucrados.'
        ),
        'total_incidencias': Incidencia.objects.count(),
        'total_categorias': Categoria.objects.count(),
        'total_estados': Estado.objects.count(),
        'total_historial': HistorialEstado.objects.count(),
    }
    return render(request, 'home.html', contexto)


def acerca(request):
    """Vista informativa sobre el proyecto municipal."""
    contexto = {
        'nombre_proyecto': 'Sistema de Reporte de Incidencias Urbanas',
    }
    return render(request, 'acerca.html', contexto)


# =============================================================================
# CRUD CBV — INCIDENCIAS
# =============================================================================

class IncidenciaListView(ListView):
    model = Incidencia
    template_name = 'incidencias_app/incidencia/listado_incidencias.html'
    context_object_name = 'incidencias'

    def get_queryset(self):
        return Incidencia.objects.select_related('categoria', 'estado').all()


class IncidenciaDetailView(DetailView):
    model = Incidencia
    template_name = 'incidencias_app/incidencia/detalle_incidencia.html'
    context_object_name = 'incidencia'

    def get_queryset(self):
        return Incidencia.objects.select_related('categoria', 'estado').prefetch_related(
            'historial_estados__estado_anterior',
            'historial_estados__estado_nuevo',
        )


class IncidenciaCreateView(CreateView):
    model = Incidencia
    form_class = IncidenciaForm
    template_name = 'incidencias_app/incidencia/formulario_incidencia.html'
    success_url = reverse_lazy('incidencias_app:incidencia_list')

    @transaction.atomic
    def form_valid(self, form):
        self.object = form.save()
        HistorialEstado.objects.create(
            incidencia=self.object,
            estado_nuevo=self.object.estado,
            observacion='Estado inicial registrado desde formulario web',
        )
        messages.success(
            self.request,
            f'Incidencia "{self.object.titulo}" creada correctamente.',
        )
        return HttpResponseRedirect(self.get_success_url())


class IncidenciaUpdateView(UpdateView):
    model = Incidencia
    form_class = IncidenciaForm
    template_name = 'incidencias_app/incidencia/formulario_incidencia.html'
    success_url = reverse_lazy('incidencias_app:incidencia_list')

    @transaction.atomic
    def form_valid(self, form):
        estado_anterior_id = Incidencia.objects.get(pk=self.object.pk).estado_id
        self.object = form.save()
        if estado_anterior_id != self.object.estado_id:
            HistorialEstado.objects.create(
                incidencia=self.object,
                estado_anterior_id=estado_anterior_id,
                estado_nuevo=self.object.estado,
                observacion='Cambio de estado registrado desde formulario web',
            )
        messages.success(
            self.request,
            f'Incidencia "{self.object.titulo}" actualizada correctamente.',
        )
        return HttpResponseRedirect(self.get_success_url())


class IncidenciaDeleteView(DeleteView):
    model = Incidencia
    template_name = 'incidencias_app/incidencia/eliminar_incidencia.html'
    context_object_name = 'incidencia'
    success_url = reverse_lazy('incidencias_app:incidencia_list')

    def form_valid(self, form):
        titulo = self.object.titulo
        response = super().form_valid(form)
        messages.success(self.request, f'Incidencia "{titulo}" eliminada correctamente.')
        return response


# =============================================================================
# CRUD CBV — CATEGORÍAS
# =============================================================================

class CategoriaListView(ListView):
    model = Categoria
    template_name = 'incidencias_app/categoria/listado_categorias.html'
    context_object_name = 'categorias'


class CategoriaDetailView(DetailView):
    model = Categoria
    template_name = 'incidencias_app/categoria/detalle_categoria.html'
    context_object_name = 'categoria'

    def get_queryset(self):
        return Categoria.objects.prefetch_related('incidencias__estado')


class CategoriaCreateView(CreateView):
    model = Categoria
    form_class = CategoriaForm
    template_name = 'incidencias_app/categoria/formulario_categoria.html'
    success_url = reverse_lazy('incidencias_app:categoria_list')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(
            self.request,
            f'Categoría "{self.object.nombre}" creada correctamente.',
        )
        return response


class CategoriaUpdateView(UpdateView):
    model = Categoria
    form_class = CategoriaForm
    template_name = 'incidencias_app/categoria/formulario_categoria.html'
    success_url = reverse_lazy('incidencias_app:categoria_list')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(
            self.request,
            f'Categoría "{self.object.nombre}" actualizada correctamente.',
        )
        return response


class CategoriaDeleteView(DeleteView):
    model = Categoria
    template_name = 'incidencias_app/categoria/eliminar_categoria.html'
    context_object_name = 'categoria'
    success_url = reverse_lazy('incidencias_app:categoria_list')

    def form_valid(self, form):
        nombre = self.object.nombre
        try:
            response = super().form_valid(form)
        except ProtectedError:
            messages.error(
                self.request,
                f'No se puede eliminar la categoría "{nombre}" porque tiene incidencias asociadas.',
            )
            return redirect('incidencias_app:categoria_list')
        messages.success(self.request, f'Categoría "{nombre}" eliminada correctamente.')
        return response


# =============================================================================
# CRUD CBV — ESTADOS
# =============================================================================

class EstadoListView(ListView):
    model = Estado
    template_name = 'incidencias_app/estado/listado_estados.html'
    context_object_name = 'estados'


class EstadoDetailView(DetailView):
    model = Estado
    template_name = 'incidencias_app/estado/detalle_estado.html'
    context_object_name = 'estado'

    def get_queryset(self):
        return Estado.objects.prefetch_related('incidencias__categoria')


class EstadoCreateView(CreateView):
    model = Estado
    form_class = EstadoForm
    template_name = 'incidencias_app/estado/formulario_estado.html'
    success_url = reverse_lazy('incidencias_app:estado_list')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(
            self.request,
            f'Estado "{self.object.nombre}" creado correctamente.',
        )
        return response


class EstadoUpdateView(UpdateView):
    model = Estado
    form_class = EstadoForm
    template_name = 'incidencias_app/estado/formulario_estado.html'
    success_url = reverse_lazy('incidencias_app:estado_list')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(
            self.request,
            f'Estado "{self.object.nombre}" actualizado correctamente.',
        )
        return response


class EstadoDeleteView(DeleteView):
    model = Estado
    template_name = 'incidencias_app/estado/eliminar_estado.html'
    context_object_name = 'estado'
    success_url = reverse_lazy('incidencias_app:estado_list')

    def form_valid(self, form):
        nombre = self.object.nombre
        try:
            response = super().form_valid(form)
        except ProtectedError:
            messages.error(
                self.request,
                f'No se puede eliminar el estado "{nombre}" porque está referenciado por incidencias o por el historial de auditoría.',
            )
            return redirect('incidencias_app:estado_list')
        messages.success(self.request, f'Estado "{nombre}" eliminado correctamente.')
        return response


# =============================================================================
# CONSULTA CBV — HISTORIAL DE ESTADOS (SOLO LECTURA POR AUDITORÍA)
# =============================================================================

class HistorialEstadoListView(ListView):
    model = HistorialEstado
    template_name = 'incidencias_app/historial/listado_historial.html'
    context_object_name = 'registros'

    def get_queryset(self):
        return HistorialEstado.objects.select_related(
            'incidencia', 'estado_anterior', 'estado_nuevo'
        ).all()


class HistorialEstadoDetailView(DetailView):
    model = HistorialEstado
    template_name = 'incidencias_app/historial/detalle_historial.html'
    context_object_name = 'registro'

    def get_queryset(self):
        return HistorialEstado.objects.select_related(
            'incidencia', 'estado_anterior', 'estado_nuevo'
        )