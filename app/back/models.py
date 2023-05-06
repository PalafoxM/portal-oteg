from django.db import models
from django.forms import model_to_dict
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField


class EcosistemaManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().using('ecosistema')

# Create your models here.

class Banner(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nombre")
    banner_url = models.CharField(max_length=100, verbose_name="Enlace")
    publication = models.BooleanField(default=True)
    imagen = models.ImageField(null=True, blank=True, upload_to='images/')
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
    nombre_categoria = models.CharField(max_length=100, null=True, blank=True)
    fecha_creacion = models.DateField()
    publicacion = models.BooleanField(default=False, null=True, blank=True)
    visible = models.BooleanField(default=True, null=True, blank=True)
    seccion = models.ForeignKey(
        SeccionesCentroDocumental, on_delete=models.CASCADE, null=True, blank=True)


class Publications(models.Model):

    TYPE_CHOICES = (
        ('1', 'PDF'),
        ('2', 'MP3'),
        ('3', 'XLS'),
    )

    section = models.ForeignKey(
        SeccionesCentroDocumental, on_delete=models.CASCADE, null=True, blank=True)
    category = models.ForeignKey(
        Categorias, on_delete=models.CASCADE, null=True, blank=True)
    publication = models.BooleanField(default=True)
    visible = models.BooleanField(default=True)
    recent = models.BooleanField(default=True)
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    num_descargas = models.IntegerField(null=True, blank=True, default=0)
    name = models.CharField(max_length=100, verbose_name="Nombre")
    url = models.URLField(max_length=100, null=True, blank=True)
    date_created = models.DateTimeField(auto_now=True)
    num_descargas = models.IntegerField(null=True, blank=True, default=0)

    


class Evento (models.Model):
    titulo = models.CharField(max_length=100)
    descripcion = models.TextField()
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    tipo_evento = models.TextField()
    tipo_evento1 = models.TextField()
    imagen = models.ImageField(upload_to='images/')
    date_updated = models.DateTimeField(auto_now=True,)
    date_created = models.DateTimeField(auto_now=True)

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
    descripcion = RichTextField()
    sitio_web = models.URLField()
    imagen = models.ImageField(null=True, blank=True, upload_to='images/')
    fecha_nota = models.DateField()
    autor_foto = models.CharField(max_length=100)
    autor_nota = models.CharField(max_length=100)
    fecha_recuperacion = models.DateField()


class Glosario (models.Model):
    palabra = models.CharField(max_length=100, null=True, blank=True)
    definicion = models.CharField(max_length=100, null=True, blank=True)


class Alba(models.Model):
    archivo = models.ImageField(null=True, blank=True, upload_to='pdf/')
    visible = models.BooleanField(default=True)
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

# #Fuentes de Informacion


class catalogo_categorias(models.Model):
    # db = 'db2'
    categoria = models.CharField(max_length=100, null=True, blank=True)




class catalogo_destinos(models.Model):
    destino = models.CharField(max_length=100, null=True, blank=True)


class DataTour (models.Model):
    fecha = models.DateField()
    destino = models.CharField(max_length=255)
    categoria = models.CharField(max_length=255)
    cuartos_registrados = models.IntegerField()
    cuartos_disponibles = models.IntegerField()
    cuartos_disponibles_prom = models.IntegerField()
    cuartos_ocupados = models.IntegerField()
    cuartos_ocupados_residentes = models.IntegerField()
    cuartos_ocupados_no_residentes = models.IntegerField()
    llegadas_turistas = models.IntegerField()
    llegadas_turistas_residentes = models.IntegerField()
    llegadas_turistas_no_residentes = models.IntegerField()
    turistas_noche = models.IntegerField()
    turistas_noche_residentes = models.IntegerField()
    turistas_noche_no_residentes = models.IntegerField()
    porcentaje_ocupacion = models.FloatField()
    porcentaje_ocupacion_residentes = models.FloatField()
    porcentaje_ocupacion_no_residentes = models.FloatField()
    estadia_promedio = models.FloatField()
    estadia_promedio_residentes = models.FloatField()
    estadia_promedio_no_residentes = models.FloatField()
    densidad_ocupacion = models.FloatField()
    densidad_ocupacion_residentes = models.FloatField()
    densidad_ocupacion_no_residentes = models.FloatField()
    fecha_recuperacion = models.DateTimeField(auto_now=True)

# Fuentes informacion


class GastoDerrama(models.Model):
    anio = models.IntegerField()
    categoria = models.CharField(max_length=255)
    destino = models.CharField(max_length=255)
    gasto_diario_promedio = models.FloatField()
    participacion = models.FloatField()
    estadia_promedio = models.FloatField()


# Fuentes informacion
class otros_anuales(models.Model):
    anio = models.IntegerField()
    pib_total_sector_72 = models.FloatField()
    pib_total_de_actividades_terciarias = models.FloatField()
    basura_generada_por_persona_diaria = models.FloatField()


class zonas_arqueologicas_museos(models.Model):
    destino = models.CharField(max_length=255)
    museo_zona_arqueologica = models.CharField(max_length=455)
    fecha = models.DateField()
    origen_visitante = models.CharField(max_length=455)
    visitantes = models.IntegerField()
    tipo = models.CharField(max_length=455, null=True, blank=True)


class catalogo_zonaz_arq_museos (models.Model):
    museo_zona_arqueologica = models.CharField(max_length=455)
    tipo = models.CharField(max_length=455)

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
        db_table = "inventario_hotelero_gto"
        ordering = ['-id']

class InversionPublica(models.Model):
    fecha = models.DateField()
    destino = models.CharField(max_length=255)
    monto_total = models.FloatField()
    nombre_de_la_obra = models.CharField(max_length=255)
    monto_de_inversion_municipal = models.FloatField()
    monto_de_inversion_estatal = models.FloatField()
    monto_de_inversion_federal = models.FloatField()

    def __str__(self):
        return f"{self.destino} - {self.nombre_de_la_obra} ({self.fecha})"

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


class CalidadAire(models.Model):
    fecha = models.DateField()
    destino = models.CharField(max_length=555)
    calidad_del_aire = models.CharField(max_length=2255)

    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        verbose_name = 'aire'
        verbose_name_plural = 'aire'
        db_table = 'aire'
        ordering = ['-id']


# catalagos para destino y categoriaclass Categoria(models.Model):
class CatalagoCategoria(models.Model):
    categoria = models.CharField(max_length=255)

class CatalagoDestino(models.Model):
    destino = models.CharField(max_length=455)
    entidad = models.CharField(max_length=455)