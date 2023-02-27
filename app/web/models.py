from django.db import models

# Create your models here.

#seccion 1 = Perfil de Visitante a Ciudad
#seccion 2 = Perfil de Visitante a Evento
#seccion 3 = Marco Normativo de Turismo
#seccion 4 = Noticias Turísticas
#seccion 5 = Sustentabilidad
# .......



class PerfilVisistantePDF (models.Model):
    seccion = models.IntegerField(null=True, blank=False)
    subseccion = models.CharField(max_length=100, null=True, blank=True)
    nombrePDF = models.CharField(max_length=100, null=True, blank=True)
    url = models.URLField(max_length=100, null=True, blank=True)
    yearPDF = models.IntegerField(null=True, blank=False)
    num_descargas = models.IntegerField(null=True, blank=True, default=0)
    fecha_registro = models.DateTimeField(auto_now_add=True, null=True, blank=True)

class BarometroTuristico (models.Model):
    semestre = models.IntegerField(null=True, blank=False)
    nombrePDF = models.CharField(max_length=100, null=True, blank=True)
    url = models.URLField(max_length=100, null=True, blank=True)
    yearPDF = models.IntegerField(null=True, blank=False)
    num_descargas = models.IntegerField(null=True, blank=True, default=0)
    fecha_registro = models.DateTimeField(auto_now_add=True, null=True, blank=True)