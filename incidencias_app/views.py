from django.shortcuts import render


def home(request):
    """
    Vista de bienvenida del sistema.

    Reemplaza la página por defecto de Django y presenta el proyecto:
    Sistema de Reporte de Incidencias Urbanas para la Municipalidad.
    """
    contexto = {
        'nombre_proyecto': 'Sistema de Reporte de Incidencias Urbanas',
        'descripcion': (
            'Plataforma que permite a ciudadanos y gestores municipales '
            'registrar, dar seguimiento y auditar incidencias urbanas '
            '(baches, luminarias, basura, semáforos, etc.), centralizando '
            'la información histórica y facilitando la coordinación entre '
            'los distintos actores involucrados.'
        ),
    }
    return render(request, 'home.html', contexto)


def acerca(request):
    """Vista de ejemplo adicional: información sobre el proyecto."""
    contexto = {
        'nombre_proyecto': 'Sistema de Reporte de Incidencias Urbanas',
    }
    return render(request, 'acerca.html', contexto)
