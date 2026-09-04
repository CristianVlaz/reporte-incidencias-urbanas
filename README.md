# Sistema de Reporte de Incidencias Urbanas

Proyecto 30 - Programación Backend, INACAP 2026.

## Descripción

La Municipalidad necesita digitalizar la gestión de incidencias urbanas. Esta
plataforma centralizará la información hoy distribuida en distintos
registros, permitiendo a ciudadanos y gestores municipales operar sobre los
reportes, mantener históricos, controlar situaciones excepcionales y auditar
los cambios de estado.

Esta primera entrega (**Evaluación 1**) construye la base técnica del
backend: repositorio Git, ambiente virtual, núcleo Django y una aplicación
(`incidencias_app`) con rutas propias, página de bienvenida y página de
error 404 personalizada. El modelo de datos y el CRUD se incorporan en la
siguiente evaluación.

## Requisitos previos

- Python 3.11 o superior
- Git
- Un editor de código (recomendado: Visual Studio Code)

## Instalación y ejecución

1. Clonar el repositorio:
   ```bash
   git clone <URL_DE_TU_REPOSITORIO>
   cd <carpeta_del_proyecto>
   ```

2. Crear el ambiente virtual:
   ```bash
   python -m venv .venv
   ```

3. Activar el ambiente virtual:
   - **Windows (PowerShell):**
     ```powershell
     .venv\Scripts\Activate
     ```
     Si aparece un error de permisos, ejecutar una vez:
     ```powershell
     Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
     ```
   - **Windows (CMD):**
     ```cmd
     .venv\Scripts\activate.bat
     ```
   - **macOS / Linux:**
     ```bash
     source .venv/bin/activate
     ```

4. Instalar las dependencias:
   ```bash
   pip install -r requirements.txt
   ```

5. Ejecutar el servidor de desarrollo:
   ```bash
   python manage.py runserver
   ```

6. Abrir en el navegador:
   - Página de bienvenida: http://127.0.0.1:8000/
   - Acerca del proyecto: http://127.0.0.1:8000/acerca/
   - Página 404: ingresar cualquier URL inexistente, por ejemplo
     http://127.0.0.1:8000/no-existe/

Para desactivar el ambiente virtual cuando termines:
```bash
deactivate
```

## Estructura del proyecto

```
├── core/                  # Núcleo del proyecto Django (configuración, urls raíz)
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── incidencias_app/       # Aplicación del proyecto
│   ├── views.py           # Vista de bienvenida y vista "acerca"
│   ├── urls.py            # Rutas propias de la app
│   ├── models.py          # (se completa en la Evaluación 2)
│   └── admin.py
├── templates/              # Plantillas HTML (base, home, acerca, 404)
├── static/css/style.css    # Estilos del sitio
├── requirements.txt
├── manage.py
└── .gitignore
```

## Notas para la evaluación

- El proyecto se ejecuta dentro de un ambiente virtual propio (`.venv`), que
  no se sube al repositorio.
- La ruta raíz (`core/urls.py`) delega a `incidencias_app/urls.py` mediante
  `include()`, cumpliendo con el requisito de rutas propias de la aplicación.
- La página 404 solo se muestra personalizada cuando `DEBUG = False` en
  `core/settings.py`. Recuerda dejarla en `False` al momento de demostrarla
  al profesor.
