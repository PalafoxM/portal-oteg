from django.db import models


# Create your models here.
class SeccionesCentroDocumental(models.Model):
    seccion = models.CharField(max_length=100)
    descripcion = models.TextField()
    observacion = models.TextField(blank=True, null=True)


class Categorias(models.Model):
    nombre_categoria = models.CharField(max_length=100)
    fecha_creacion = models.DateField()
    publicacion = models.BooleanField(default=False)
    visible = models.BooleanField(default=True)
    seccion = models.ForeignKey(SeccionesCentroDocumental, on_delete=models.CASCADE , null=True, blank=True)

