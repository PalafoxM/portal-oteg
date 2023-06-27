from django.db import models
from storages.backends.s3boto3 import S3Boto3Storage
import os
from django.core.validators import FileExtensionValidator



class S3Storage(S3Boto3Storage):
    location = 'media'  # Carpeta dentro del bucket donde se almacenarán las imágenes
    file_overwrite = False  # No sobrescribir archivos existentes con el mismo nombre
    bucket_name = os.getenv('AWS_BUCKET')
    access_key = os.getenv('AWS_ACCESS_KEY_ID')
    secret_key = os.getenv('AWS_SECRET_ACCESS_KEY')


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
    # url = models.FileField(upload_to='barometro-turistico', storage=S3Storage(), verbose_name="Archivo", blank=True)#
    doc = models.FileField(upload_to='barometro-turistico', storage=S3Storage(), verbose_name="Documento", blank=True)#
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