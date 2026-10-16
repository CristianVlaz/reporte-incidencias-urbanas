# Sistema de Reporte de Incidencias Urbanas — Evaluación 2

Continuación **del proyecto original de la Evaluación 1**, para la asignatura Programación Backend (INACAP 2026). Mantiene sus páginas `/`, `/acerca/` y su plantilla 404.

## Alcance
- ORM Django: `Categoria`, `Estado`, `Incidencia`, `HistorialEstado`.
- Relaciones: cada incidencia pertenece a una categoría y a un estado; tiene múltiples registros en su historial.
- Django REST Framework: serializers + ModelViewSet + DefaultRouter.
- CRUD completo para **Categoría, Estado e Incidencia** mediante GET, POST, PUT, PATCH y DELETE.
- Historial de estados consultable en GET y actualizado automáticamente al crear o cambiar el estado de una incidencia mediante API o Django Admin. **Es solo lectura por diseño** para evitar falsificar la auditoría.
- MySQL con tres scripts SQL. Variables de entorno gestionadas mediante `python-decouple`.
- Datos semilla (fixtures), migración inicial y tests.

## Instalación
Sigue primero **`GUIA_INSTALACION_WINDOWS.md`**, que incluye cada clic/orden de instalación y una guía de demostración.

## Arquitectura
```text
core/                  settings.py, urls.py
incidencias_app/       models.py, admin.py, views.py, urls.py (páginas anteriores)
                       serializers.py, api_views.py, api_urls.py
                       migrations/0001_initial.py
                       fixtures/datos_iniciales.json, tests.py
sql/                   01_crear_base_datos.sql, 02_crear_usuario.sql, 03_asignar_permisos.sql
templates/             páginas HTML originales
static/                CSS original
.env.example           plantilla de configuración; copiar a .env (no subir)
requirements.txt       dependencias
```

## Endpoints
| URL | GET lista | POST | GET detalle | PUT | PATCH | DELETE |
|---|---|---|---|---|---|---|
| `/api/categorias/` | Sí | Sí | `/api/categorias/<id>/` | Sí | Sí | Sí |
| `/api/estados/` | Sí | Sí | `/api/estados/<id>/` | Sí | Sí | Sí |
| `/api/incidencias/` | Sí | Sí | `/api/incidencias/<id>/` | Sí | Sí | Sí |
| `/api/historial-estados/` | Sí | No | `/api/historial-estados/<id>/` | No | No | No |

Nota: las rutas de lista aceptan GET y POST; los métodos PUT/PATCH/DELETE operan sobre la URL de detalle terminada en `/id/`.

## Ejemplos de datos
Crear una incidencia con `POST /api/incidencias/`:
```json
{
  "titulo": "Luminaria apagada", "descripcion": "La luz no enciende hace dos días",
  "direccion": "Av. Principal 123", "comuna": "Temuco",
  "categoria": 2, "estado": 1, "prioridad": "alta",
  "nombre_reportante": "Vecino de prueba", "correo_reportante": "vecino@example.com"
}
```
Los IDs de categorías/estados del ejemplo asumen que se cargó `datos_iniciales.json` en una base vacía. Verificar con GET antes de usar.

## Comandos rápidos
```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
Copy-Item .env.example .env
# Editar .env, y ejecutar los SQL antes de migrar (MySQL).
python manage.py check
python manage.py migrate
python manage.py loaddata datos_iniciales
python manage.py createsuperuser
python manage.py test
python manage.py runserver
```

## Precauciones
Esta API es para **demostración local**, con permisos de escritura abiertos por diseño académico. **No publicar en Internet** sin autenticación/autorización, HTTPS, validaciones y ajustes de seguridad. `.env`, claves y base de datos local no se suben a GitHub.

## Entrega pendiente del estudiante
El ZIP incluye código, scripts y migración, pero debes **instalar dependencias, crear/ejecutar la base de datos MySQL en tu PC, ejecutar pruebas y migraciones**, subir a TU repositorio y aportar la URL real junto con capturas de evidencia. Se adjunta `CHECKLIST_ENTREGA.md`.
