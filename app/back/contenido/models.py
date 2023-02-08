from django.db import models

# Create your models here.
class Banner(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nombre")
    banner_url = models.CharField(max_length=100, verbose_name="Enlace")
    publication = models.BooleanField(default=True)
    img_url = models.CharField(max_length=100, verbose_name="Imagen")
    fiel = models.FileField(upload_to='archivo/%y/%m/%d', null=True, blank=True)
    date_created = models.DateTimeField(auto_now=True)

def __str__(self):
    return self.name


class Meta:
    verbose_name = 'Banner'
    verbose_name_plural = 'Banners'
    db_table = 'banners'
    ordering = ['-id']