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
    publication = models.BooleanField(default=True, verbose_name="Publicación")
    imagen = models.ImageField(null=True, blank=True ,upload_to='images/')
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
    sitio_web = models.URLField(verbose_name="Link")
    decription = models.CharField(max_length=100, verbose_name="Descripcion")
    date_created = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.sitio_web
    
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
    fecha_fin = models.DateField()
    tipo_evento = models.TextField()
    tipo_evento1 = models.TextField()
    imagen = models.ImageField(upload_to='images/')

    def __str__(self):
        return self.titulo

    def toJSON(self):
        # item = model_to_dict(self)
        return {
            "id": self.id,
            "titulo": self.titulo,
            "descripcion": self.descripcion,
            "fecha_inicio": self.fecha_inicio,
            "fecha_fin": self.fecha_fin,
            "tipo_evento": self.tipo_evento,
        }

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

    # def __str__(self):
    #     return self.visible
    
    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        verbose_name = 'alba'
        verbose_name_plural = 'alba'
        db_table = 'alba'
        ordering = ['-id']


class InventarioHotelero(models.Model):
    
    destino = models.CharField(max_length=255)
    fecha = models.DateField()
    categoria = models.CharField(max_length=255)
    habitaciones = models.IntegerField()
    establecimientos = models.IntegerField()
    date_updated = models.DateTimeField(auto_now=True,)
    date_created = models.DateTimeField(auto_now=True)
    
    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        verbose_name = 'inventario_hotelero_gto'
        verbose_name_plural = 'inventario_hotelero_gto'
        db_table = 'inventario_hotelero_gto'
        ordering = ['-id']

class InversionPublica(models.Model):
    fecha = models.DateField()
    municipio = models.CharField(max_length=255)
    nombre_obra = models.CharField(max_length=255)
    monto_inversion_municipal = models.FloatField()
    monto_inversion_estatal = models.FloatField()
    monto_inversion_federal = models.FloatField()

    def __str__(self):
        return f"{self.municipio} - {self.nombre_obra} ({self.fecha})"

    def toJSON(self):
        """
        Método para serializar el objeto a formato JSON.
        """
        item = model_to_dict(self)
        return item

    class Meta:
        verbose_name_plural = "Inversiones Públicas"
        db_table = "inversion_publica"
        ordering = ['-id']

class InventarioHoteleroEntNac(models.Model):
    
    destino = models.CharField(max_length=255)
    fecha = models.DateField()
    categoria = models.CharField(max_length=255)
    habitaciones = models.IntegerField()
    establecimientos = models.IntegerField()
    date_updated = models.DateTimeField(auto_now=True,)
    date_created = models.DateTimeField(auto_now=True)
    
    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        verbose_name = 'inventario_hotelero_ent_nac'
        verbose_name_plural = 'inventario_hotelero_ent_nac'
        db_table = 'inventario_hotelero_ent_nac'
        ordering = ['-id']