# Migración inicial de la Evaluación 2.
import django.db.models.deletion
from django.db import migrations, models

class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [
        migrations.CreateModel(
            name='Categoria',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=80, unique=True)),
                ('descripcion', models.TextField(blank=True)),
                ('activo', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={'verbose_name': 'Categoría', 'verbose_name_plural': 'Categorías', 'ordering': ['nombre']},
        ),
        migrations.CreateModel(
            name='Estado',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=60, unique=True)),
                ('descripcion', models.TextField(blank=True)),
                ('es_final', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={'verbose_name': 'Estado', 'verbose_name_plural': 'Estados', 'ordering': ['id']},
        ),
        migrations.CreateModel(
            name='Incidencia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=150)),
                ('descripcion', models.TextField()),
                ('direccion', models.CharField(max_length=255)),
                ('comuna', models.CharField(max_length=100)),
                ('prioridad', models.CharField(choices=[('baja', 'Baja'), ('media', 'Media'), ('alta', 'Alta'), ('critica', 'Crítica')], default='media', max_length=10)),
                ('nombre_reportante', models.CharField(max_length=120)),
                ('correo_reportante', models.EmailField(blank=True, max_length=254)),
                ('fecha_reporte', models.DateTimeField(auto_now_add=True)),
                ('fecha_actualizacion', models.DateTimeField(auto_now=True)),
                ('categoria', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='incidencias', to='incidencias_app.categoria')),
                ('estado', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='incidencias', to='incidencias_app.estado')),
            ],
            options={'verbose_name': 'Incidencia', 'verbose_name_plural': 'Incidencias', 'ordering': ['-fecha_reporte']},
        ),
        migrations.CreateModel(
            name='HistorialEstado',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('observacion', models.TextField(blank=True)),
                ('fecha_cambio', models.DateTimeField(auto_now_add=True)),
                ('estado_anterior', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='historial_anterior', to='incidencias_app.estado')),
                ('estado_nuevo', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='historial_nuevo', to='incidencias_app.estado')),
                ('incidencia', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='historial_estados', to='incidencias_app.incidencia')),
            ],
            options={'verbose_name': 'Cambio de estado', 'verbose_name_plural': 'Historial de estados', 'ordering': ['-fecha_cambio']},
        ),
    ]
