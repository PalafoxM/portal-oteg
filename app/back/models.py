from django.db import models
from django.forms import model_to_dict
from django.contrib.auth.models import User

# Create your models here.
class Publications(models.Model):
    section = models.CharField(max_length=100, verbose_name="Sección")
    category = models.CharField(max_length=100, verbose_name="Categoria")
    publication = models.BooleanField(default=True)
    visible =  models.BooleanField(default=True)
    recent = models.BooleanField(default=True)
    type = models.CharField(max_length=100, verbose_name="Tipo")
    download = models.CharField(max_length=100, verbose_name="Descarga")
    name = models.CharField(max_length=100, verbose_name="Nombre")
    fiel = models.FileField(upload_to='archivo/%y/%m/%d', null=True, blank=True)
    date_created = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.publication
    
    def toJSON(self):
        item = model_to_dict(self)
        return item


    class Meta:
        verbose_name = 'Publicación'
        verbose_name_plural = 'Publicaciones'
        db_table = 'publications'
        ordering = ['-id']

class Banner(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nombre")
    banner_url = models.CharField(max_length=100, verbose_name="Enlace")
    publication = models.BooleanField(default=True)
    img_url = models.CharField(max_length=100, verbose_name="Imagen")
    fiel = models.FileField(upload_to='archivo/%y/%m/%d', null=True, blank=True)
    date_created = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
    def toJSON(self):
        item = model_to_dict(self)
        return item
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
    
    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        verbose_name = 'places_of_interest'
        verbose_name_plural = 'places_of_interest'
        db_table = 'places_of_interest'
        ordering = ['-id']

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

class Evento (models.Model):
    titulo = models.CharField(max_length=100)
    descripcion = models.TextField()
    fecha_inicio = models.DateField()
    imagen = models.ImageField(null=True, blank=True ,upload_to='images/')

class Noticia (models.Model):
    titulo = models.CharField(max_length=100)
    descripcion = models.TextField()
    sitio_web = models.URLField()
    imagen = models.ImageField(null=True, blank=True ,upload_to='images/')
    fecha_nota = models.DateField()
    autor_foto = models.CharField(max_length=100)
    autor_nota = models.CharField(max_length=100)
    fecha_recuperacion = models.DateField()

class Alba(models.Model):
    archivo = models.ImageField(null=True, blank=True ,upload_to='pdf/')
    visible =  models.BooleanField(default=True)
    date_updated = models.DateTimeField(auto_now=True,)
    date_created = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.visible
    
    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        verbose_name = 'alba'
        verbose_name_plural = 'alba'
        db_table = 'alba'
        ordering = ['-id']
