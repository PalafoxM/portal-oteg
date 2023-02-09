from django.db import models
from django.forms import model_to_dict

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

class PlacesOfInterest(models.Model):
    logotipo = models.CharField(max_length=100, verbose_name="Logotipo")
    sito_web = models.CharField(max_length=100, verbose_name="Link")
    decription = models.CharField(max_length=100, verbose_name="Descripcion")
    date_created = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.sito_web
    
    # def toJSON(self):
    #     item = model_to_dict(self)
    #     return item


    class Meta:
        verbose_name = 'places_of_interest'
        verbose_name_plural = 'places_of_interest'
        db_table = 'places_of_interest'
        ordering = ['-id']