from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User,null=True, on_delete=models.CASCADE)
    apellido_paterno = models.CharField(max_length=100, null=True, blank=True)
    apellido_materno  = models.CharField(max_length=100, null=True, blank=True)
    fecha_cumple = models.DateField(null=True, blank=True)
    direccion = models.CharField(max_length=100, null=True, blank=True)
    tel = models.CharField(max_length=100, null=True, blank=True)
    facebook = models.CharField(max_length=100, null=True, blank=True)
    twitter = models.CharField(max_length=100, null=True, blank=True)
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
    photo = models.ImageField(null=True, blank=True, upload_to='images/profile/')
    experiencia = models.TextField(null=True, blank=True)
    boletin = models.BooleanField(default=False)
    fecha_registro = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return str(self.user)

