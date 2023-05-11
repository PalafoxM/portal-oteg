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
    imagen = models.ImageField(upload_to='images/', null=True, blank=True)
    
    
class BarometroTuristico (models.Model):
    semestre = models.IntegerField(null=True, blank=False)
    nombrePDF = models.CharField(max_length=100, null=True, blank=True)
    url = models.URLField(max_length=100, null=True, blank=True)
    yearPDF = models.IntegerField(null=True, blank=False)
    num_descargas = models.IntegerField(null=True, blank=True, default=0)
    fecha_registro = models.DateTimeField(auto_now_add=True, null=True, blank=True)




class DataPoint(models.Model):
    fecha_registro = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    year = models.IntegerField(null=True, blank=False)
    enero_data = models.IntegerField(null=True, blank=True)
    febrero_data = models.IntegerField(null=True, blank=True)
    marzo_data = models.IntegerField(null=True, blank=True)
    abril_data = models.IntegerField(null=True, blank=True)
    mayo_data = models.IntegerField(null=True, blank=True)
    junio_data = models.IntegerField(null=True, blank=True)
    julio_data = models.IntegerField(null=True, blank=True)
    agosto_data = models.IntegerField(null=True, blank=True)
    septiembre_data = models.IntegerField(null=True, blank=True)
    octubre_data = models.IntegerField(null=True, blank=True)
    noviembre_data = models.IntegerField(null=True, blank=True)  
    diciembre_data = models.IntegerField(null=True, blank=True)
    estado = models.CharField(max_length=100, null=True, blank=True)

class Encuesta(models.Model):
    fecha_registro = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    url = models.URLField(max_length=100, null=True, blank=True)
    activo = models.BooleanField(default=False)
    
