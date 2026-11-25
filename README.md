# Sistema de Reporte de Incidencias Urbanas — Evaluación 3

Proyecto municipal N.º 30 para la asignatura **Programación Backend (INACAP 2026)**. Es una entrega acumulativa que integra la base Django y vista pública (Evaluación 1), el modelo ORM en MySQL + API REST con Django REST Framework (Evaluación 2) y el **CRUD web manual mediante Vistas Basadas en Clases (CBV) nativas de Django y formularios `ModelForm`** (Evaluación 3).

## Modelo de datos
- **`Categoria`**: clasificación de incidencias urbanas (`nombre`, `descripcion`, `activo`).
- **`Estado`**: etapas del ciclo de vida (`nombre`, `descripcion`, `es_final`).
- **`Incidencia`**: entidad principal relacionada con `Categoria` y `Estado` mediante `ForeignKey(..., on_delete=models.PROTECT)`.
- **`HistorialEstado`**: trazabilidad de auditoría generada automáticamente al crear una incidencia o cambiar su estado (desde la interfaz web, API REST o Django Admin).

## CRUD Web mediante CBV (Evaluación 3)
Todas las entidades principales implementan `ListView`, `DetailView`, `CreateView`, `UpdateView` y `DeleteView` registradas en `incidencias_app/urls.py`:

| Entidad | ListView | CreateView | DetailView | UpdateView | DeleteView |
|---|---|---|---|---|---|
| **Incidencia** | `/incidencias/` | `/incidencias/crear/` | `/incidencias/<id>/` | `/incidencias/<id>/editar/` | `/incidencias/<id>/eliminar/` |
| **Categoría** | `/categorias/` | `/categorias/crear/` | `/categorias/<id>/` | `/categorias/<id>/editar/` | `/categorias/<id>/eliminar/` |
| **Estado** | `/estados/` | `/estados/crear/` | `/estados/<id>/` | `/estados/<id>/editar/` | `/estados/<id>/eliminar/` |
| **HistorialEstado** | `/historial-estados/` | *Omitida (ver justificación)* | `/historial-estados/<id>/` | *Omitida (ver justificación)* | *Omitida (ver justificación)* |

### Justificación técnica de vistas omitidas en `HistorialEstado`
`HistorialEstado` implementa únicamente `ListView` y `DetailView` (y `ReadOnlyModelViewSet` en la API REST) porque corresponde a una **bitácora de auditoría inmutable**. Permitir la creación, edición o eliminación manual de registros históricos vulneraría la trazabilidad exigida por el enunciado del proyecto (*"determinados eventos producirán cambios de estado que deberán quedar registrados para efectos de auditoría y seguimiento"*). Sus registros se insertan automáticamente dentro de transacciones atómicas cuando se crea una `Incidencia` o cuando su estado cambia.

## Formularios y widgets (`incidencias_app/forms.py`)
Todos los formularios web se encuentran centralizados en `incidencias_app/forms.py` heredando de `forms.ModelForm`, separando responsabilidades respecto de `models.py` y `views.py`:
- `IncidenciaForm`: `TextInput`, `Textarea`, `Select`, `EmailInput` con clases Bootstrap (`form-control`, `form-select`), `placeholder` y `rows`.
- `CategoriaForm`: `TextInput`, `Textarea`, `CheckboxInput` (`form-check-input`).
- `EstadoForm`: `TextInput`, `Textarea`, `CheckboxInput` (`form-check-input`).

## API REST acumulativa (Evaluación 2)
| Recurso | Ruta | Métodos |
|---|---|---|
| Categorías | `/api/categorias/` | GET, POST, PUT, PATCH, DELETE |
| Estados | `/api/estados/` | GET, POST, PUT, PATCH, DELETE |
| Incidencias | `/api/incidencias/` | GET, POST, PUT, PATCH, DELETE |
| Historial de estados | `/api/historial-estados/` | GET (solo lectura) |

## Instalación y ejecución
```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
Copy-Item .env.example .env
# Configurar credenciales MySQL en .env y ejecutar los scripts de la carpeta sql/
python manage.py check
python manage.py migrate
python manage.py loaddata datos_iniciales
python manage.py test
python manage.py runserver