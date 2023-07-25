from django.db import models
from django.contrib.auth.models import User
from storages.backends.s3boto3 import S3Boto3Storage
import os
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractUser
from django.forms import model_to_dict

# Crear un RegexValidator para validar un campo numérico de 10 dígitos
validator = RegexValidator(
    regex=r'^\d{10}$',
    message='El campo debe contener exactamente 10 dígitos numéricos.'
)


class S3Storage(S3Boto3Storage):
    location = 'media'  # Carpeta dentro del bucket donde se almacenarán las imágenes
    file_overwrite = False  # No sobrescribir archivos existentes con el mismo nombre
    bucket_name = os.getenv('AWS_BUCKET')
    access_key = os.getenv('AWS_ACCESS_KEY_ID')
    secret_key = os.getenv('AWS_SECRET_ACCESS_KEY')


class Profile(models.Model):
    user = models.OneToOneField(User,null=True, on_delete=models.CASCADE)
    apellido_paterno = models.CharField(max_length=100, null=True, blank=True)
    apellido_materno  = models.CharField(max_length=100, null=True, blank=True)
    fecha_cumple = models.DateField(null=True, blank=True)
    direccion = models.CharField(max_length=100, null=True, blank=True)
    tel = models.CharField(max_length=100, null=True, blank=True,
                           validators=[RegexValidator(r'^\d{10}$', 'Ingresa un número de teléfono válido.')])
    facebook = models.URLField(max_length=100, null=True, blank=True)
    twitter = models.URLField(max_length=100, null=True, blank=True)
    ciudad = models.CharField(max_length=100, null=True, blank=True)
    estado = models.CharField(max_length=100, null=True, blank=True)
    empresa_institucion = models.CharField(max_length=100, null=True, blank=True)
    cargo = models.CharField(max_length=100, null=True, blank=True)
    licenciatura = models.CharField(max_length=100, null=True, blank=True)
    universidad_licenciatura = models.CharField(max_length=100, null=True, blank=True)
    maestria = models.CharField(max_length=100, null=True, blank=True)
    universidad_maestria = models.CharField(max_length=100, null=True, blank=True)
    doctorado = models.CharField(max_length=100, null=True, blank=True)
    universidad_doctorado = models.CharField(max_length=100, null=True, blank=True)
    photo = models.ImageField(null=True, blank=True, upload_to='profile', storage=S3Storage())
    experiencia = models.TextField(null=True, blank=True)
    boletin = models.BooleanField(default=False)
    fecha_registro = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    token = models.UUIDField(primary_key=False, editable=False, null=True, blank=True)

    def __str__(self):
        return str(self.user)
    
    class Meta:
        db_table = 'profile'
        ordering = ['-id']
