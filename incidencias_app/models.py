from django.db import models

class Categoria(models.Model):
    nombre = models.CharField(max_length=80, unique=True)
    descripcion = models.TextField(blank=True)
    activo = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['nombre']
        verbose_name = 'Categoría'
        verbose_name_plural = 'Categorías'

    def __str__(self):
        return self.nombre

class Estado(models.Model):
    nombre = models.CharField(max_length=60, unique=True)
    descripcion = models.TextField(blank=True)
    es_final = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['id']
        verbose_name = 'Estado'
        verbose_name_plural = 'Estados'

    def __str__(self):
        return self.nombre

class Incidencia(models.Model):
    class Prioridad(models.TextChoices):
        BAJA = 'baja', 'Baja'
        MEDIA = 'media', 'Media'
        ALTA = 'alta', 'Alta'
        CRITICA = 'critica', 'Crítica'

    titulo = models.CharField(max_length=150)
    descripcion = models.TextField()
    direccion = models.CharField(max_length=255)
    comuna = models.CharField(max_length=100)
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT, related_name='incidencias')
    estado = models.ForeignKey(Estado, on_delete=models.PROTECT, related_name='incidencias')
    prioridad = models.CharField(max_length=10, choices=Prioridad.choices, default=Prioridad.MEDIA)
    nombre_reportante = models.CharField(max_length=120)
    correo_reportante = models.EmailField(blank=True)
    fecha_reporte = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-fecha_reporte']
        verbose_name = 'Incidencia'
        verbose_name_plural = 'Incidencias'

    def __str__(self):
        return f'{self.id} - {self.titulo}'

class HistorialEstado(models.Model):
    incidencia = models.ForeignKey(Incidencia, on_delete=models.CASCADE, related_name='historial_estados')
    estado_anterior = models.ForeignKey(Estado, on_delete=models.PROTECT, null=True, blank=True, related_name='historial_anterior')
    estado_nuevo = models.ForeignKey(Estado, on_delete=models.PROTECT, related_name='historial_nuevo')
    observacion = models.TextField(blank=True)
    fecha_cambio = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-fecha_cambio']
        verbose_name = 'Cambio de estado'
        verbose_name_plural = 'Historial de estados'

    def __str__(self):
        return f'Incidencia {self.incidencia_id}: {self.estado_nuevo}'
