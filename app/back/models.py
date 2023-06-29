from django.db import models
from django.forms import model_to_dict
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage
import os
from django.core.validators import FileExtensionValidator


class S3Storage(S3Boto3Storage):
    location = 'media'  # Carpeta dentro del bucket donde se almacenarán las imágenes
    file_overwrite = False  # No sobrescribir archivos existentes con el mismo nombre
    bucket_name = os.getenv('AWS_BUCKET')
    access_key = os.getenv('AWS_ACCESS_KEY_ID')
    secret_key = os.getenv('AWS_SECRET_ACCESS_KEY')


class EcosistemaManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().using('ecosistema')

# Create your models here.
class Banner(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nombre")
    banner_url = models.CharField(max_length=100, verbose_name="Enlace" , null=True, blank=True)
    imagen = models.ImageField(null=True, blank=True, upload_to='banner-images', storage=S3Storage())
    date_created = models.DateTimeField(auto_now=True)
    subtitulo = models.CharField(max_length=100, verbose_name="Subtitulo" , null=True, blank=True)
    titulo_pricipal = models.CharField(max_length=100, verbose_name="Titulo Principal" , null=True, blank=True)
    activo = models.BooleanField(default=True)

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
    logotipo = models.ImageField(upload_to='logos', storage=S3Storage(), verbose_name="Logotipo")
    sitio_web = models.URLField(verbose_name="Link")
    description = models.CharField(max_length=100)
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
    url = models.FileField(null=True, blank=True, upload_to='publicacion', storage=S3Storage(), validators=[FileExtensionValidator(['pdf'])])#pdf
    date_created = models.DateTimeField(auto_now=True)
    num_descargas = models.IntegerField(null=True, blank=True, default=0)


class Evento (models.Model):
    titulo = models.CharField(max_length=100)
    descripcion = models.TextField()
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    tipo_evento = models.TextField()
    imagen = models.ImageField(upload_to='oteg', storage=S3Storage())
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
    imagen = models.ImageField(null=True, blank=True, upload_to='noticias', storage=S3Storage())
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

class Eniot(models.Model):
    nombrePDF = models.CharField(max_length=100, null=True, blank=True)
    doc_url = models.FileField(upload_to='eniot', storage=S3Storage(), verbose_name="Documento", blank=True)
    seccion = models.CharField(max_length=100, null=True, blank=True)
    num_descargas = models.IntegerField(null=True, blank=True, default=0)
    anio = models.IntegerField(null=True, blank=False)
    # aniov2 = models.IntegerField(null=True, blank=False)
    date_updated = models.DateTimeField(auto_now=True)
    date_created = models.DateTimeField(auto_now=True)

    class Meta:
        # db_table = 'eniot'
        ordering = ['-id']

    def save(self, *args, **kwargs):
        # Actualizar la ruta del documento basado en el campo 'seccion'
        if self.seccion is not None:
            filename = os.path.basename(self.doc_url.name)
            nombre_archivo, extension = os.path.splitext(filename)
            new_filename = f'{nombre_archivo}-{self.seccion}{extension}'
            self.doc_url.name = os.path.join( str(self.seccion), new_filename)

        super(Eniot, self).save(*args, **kwargs)

class EniotAlbun(models.Model):
    nombreAlbun = models.CharField(max_length=100, null=True, blank=True)
    foto_url = models.FileField(upload_to='eniot', storage=S3Storage(), verbose_name="Documento", blank=True)
    descripcion = models.CharField(max_length=100, null=True, blank=True)
    date_updated = models.DateTimeField(auto_now=True)
    date_created = models.DateTimeField(auto_now=True)

    class Meta:
        # db_table = 'eniot'
        ordering = ['-id']

    def save(self, *args, **kwargs):
        # Actualizar la ruta del documento basado en el nombre del álbum
        if self.foto_url is not None:
            filename = os.path.basename(self.foto_url.name)
            nombre_archivo, extension = os.path.splitext(filename)
            new_filename = f'{nombre_archivo}-{self.nombreAlbun}{extension}'
            self.foto_url.name = os.path.join('eniot', self.nombreAlbun, new_filename)

        super(EniotAlbun, self).save(*args, **kwargs)
        
    def get_fotos(self):
        return self.fotos.all()
    
    def get_fotos_by_nombre(self):
        return self.fotos.filter(album__nombreAlbun=self.nombreAlbun)

# #Fuentes de Informacion


class DataTour (models.Model):
    destino = models.CharField(max_length=256, null=True)
    categoria = models.CharField(max_length=256, null=True)
    fecha = models.DateField(null=True)
    cuartos_registrados_fin_periodo = models.FloatField(null=True)
    cuartos_disponibles_promedio = models.FloatField(null=True)
    cuartos_disponibles = models.FloatField(null=True)
    cuartos_ocupados = models.FloatField(null=True)
    cuartos_ocupados_residentes = models.FloatField(null=True)
    cuartos_ocupados_no_residentes = models.FloatField(null=True)
    llegadas_de_turistas = models.FloatField(null=True)
    llegadas_de_turistas_residentes = models.FloatField(null=True)
    llegadas_de_turistas_no_residentes = models.FloatField(null=True)
    turistas_noche = models.FloatField(null=True)
    turistas_noche_residentes = models.FloatField(null=True)
    turistas_noche_no_residentes = models.FloatField(null=True)
    porcentaje_de_ocupacion = models.FloatField(null=True)
    porcentaje_de_ocupacion_residentes = models.FloatField(null=True)
    porcentaje_de_ocupacion_no_residentes = models.FloatField(null=True)
    estadia_promedio = models.FloatField(null=True)
    estadia_promedio_residentes = models.FloatField(null=True)
    estadia_promedio_no_residentes = models.FloatField(null=True)
    densidad_de_ocupacion = models.FloatField(null=True)
    densidad_de_ocupacion_residentes = models.FloatField(null=True)
    densidad_de_ocupacion_no_residentes = models.FloatField(null=True)

    def toJSON(self):
        item = model_to_dict(self)
        return item


    class Meta:
        app_label = 'ecosistema'
        db_table = "datatur"
        ordering = ['-id']
# Fuentes informacion


class GastoDerrama(models.Model):
    gasto_diario_prom = models.FloatField()
    ano = models.IntegerField()
    tipo_visitante = models.CharField(max_length=256)
    destino = models.CharField(max_length=256)
    participacion_en_hospedaje = models.FloatField()
    estadia_promedio = models.FloatField()

    class Meta:
        app_label = 'ecosistema'
        db_table = "gasto_derrama"
        ordering = ['-id']


# Fuentes informacion
class otros_anuales(models.Model):
    ano = models.IntegerField()
    PIB_sector_72 = models.FloatField()
    PIB_actividades_terciarias = models.FloatField()
    basura_generada_persona_diaria_Kg = models.FloatField()

    class Meta:
        app_label = 'ecosistema'
        db_table = "otros_anuales"
        ordering = ['-id']


class zonas_arqueologicas_museos(models.Model):
    destino = models.CharField(max_length=255)
    tipo = models.CharField(max_length=455, null=True, blank=True)
    nombre = models.CharField(max_length=455)
    fecha = models.DateField()
    origen_visitante = models.CharField(max_length=455)
    visitantes = models.IntegerField()

    class Meta:

        app_label = 'ecosistema'
        db_table = "zonas_arqueologicas_museos"
        ordering = ['-id']


class InventarioHotelero(models.Model):

    destino = models.CharField(max_length=455, null=True, blank=True)
    fecha = models.DateField()
    categoria = models.CharField(max_length=255)
    habitaciones = models.IntegerField()
    establecimientos = models.IntegerField()

    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        app_label = 'ecosistema'
        verbose_name = 'inventario_hotelero_gto'
        verbose_name_plural = 'inventario_hotelero_gto'
        db_table = "inventario_hotelero_gto"
        ordering = ['-id']


class InversionPublica(models.Model):
    fecha = models.DateField()
    destino = models.CharField(max_length=455, null=True, blank=True)
    monto_total = models.FloatField()
    nombre_de_la_obra = models.CharField(max_length=255)
    monto_de_inversion_municipal = models.FloatField()
    monto_de_inversion_estatal = models.FloatField()
    monto_de_inversion_federal = models.FloatField()

    def __str__(self):
        return f"{self.destino} - {self.nombre_de_la_obra} ({self.fecha})"

    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        app_label = 'ecosistema'
        verbose_name_plural = "Inversiones Públicas"
        db_table = "inversion_publica"
        ordering = ['-id']


class InventarioHoteleroEntNac(models.Model):

    
    fecha = models.DateField()
    entidad = models.CharField(max_length=455, null=True, blank=True)
    categoria = models.CharField(max_length=255)
    establecimientos = models.IntegerField()
    habitaciones = models.IntegerField()

    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        app_label = 'ecosistema'
        verbose_name = 'inventario_hotelero_ent_nac'
        verbose_name_plural = 'inventario_hotelero_ent_nac'
        db_table = 'inventario_hotelero_ent_nac'
        ordering = ['-id']


class CalidadAire(models.Model):
    fecha = models.DateField()
    destino = models.CharField(max_length=455, null=True, blank=True)
    calidad_del_aire = models.CharField(max_length=2255)

    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        app_label = 'ecosistema'
        verbose_name = 'aire'
        verbose_name_plural = 'aire'
        db_table = 'aire'
        ordering = ['-id']


class Sensivilizacion(models.Model):
    fecha = models.DateField()
    destino = models.CharField(max_length=455, null=True, blank=True)
    participantes = models.IntegerField()
    accion_de_sensibilizacion = models.CharField(max_length=455, null=True, blank=True)
    # subcategoria = models.CharField(max_length=455, null=True, blank=True)

    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        app_label = 'ecosistema'
        db_table = 'sensivilizacion'


class ProyectoInversion(models.Model):
    destino = models.CharField(max_length=256)
    id_del_proyecto = models.AutoField(primary_key=True)
    nombre_del_proyecto = models.CharField(max_length=256)
    promotor_del_proyecto = models.CharField(max_length=256, blank=True)
    referencia_de_ubicacion = models.CharField(max_length=256, blank=True)
    zona_turistica = models.CharField(max_length=256, blank=True)
    giro = models.CharField(max_length=256, blank=True)
    habitaciones = models.FloatField(blank=True, null=True)
    empleos_permanentes = models.FloatField(blank=True, null=True)
    empleos_temporales = models.FloatField(blank=True, null=True)
    tipo_de_inversion = models.CharField(max_length=256, blank=True)
    origen_de_inversion = models.CharField(max_length=256, blank=True)
    estatus = models.CharField(max_length=256, blank=True)
    fecha_de_inicio_de_obra = models.DateField(blank=True, null=True)
    fecha_de_conclusion_de_obra = models.DateField(blank=True, null=True)
    fecha_de_apertura = models.DateField(blank=True, null=True)
    monto_comprometido_del_proyecto_mxn = models.FloatField(
        blank=True, null=True)
    plazo = models.FloatField(blank=True, null=True)
    personas_beneficiadas_con_el_proyecto = models.FloatField(
        blank=True, null=True)
    datos_de_contacto = models.TextField(blank=True)

    def __str__(self):
        return self.nombre_del_proyecto
    
    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        app_label = 'ecosistema'
        db_table = 'proyectos_inversion'
        ordering = ['-id_del_proyecto']

# catalagos
class CatalagoCategoria(models.Model):
    categoria = models.CharField(max_length=255, unique=True)

    class Meta:
        app_label = 'ecosistema'
        db_table = 'catalogo_categorias'
        ordering = ['-id']


class CatalagoDestino(models.Model):
    destino = models.CharField(max_length=455, null=True, blank=True)
    entidad = models.CharField(max_length=455)

    class Meta:
        app_label = 'ecosistema'
        db_table = 'catalogo_destinos'
        ordering = ['-id']

class CatalagoDestinoAeropuerto(models.Model):
    destino_aeropuerto = models.CharField(max_length=455, null=True, blank=True)
    destino_aeropuerto_id = models.CharField(max_length=455)

    class Meta:
        app_label = 'ecosistema'
        db_table = 'catalogo_destino_aeropuerto'
        ordering = ['-id']

class CatalagoSegmentos(models.Model):
    segmento = models.CharField(max_length=455, unique=True)

    class Meta:
        app_label = 'ecosistema'
        db_table = 'catalogo_segmentos'
        ordering = ['-id']


class CatalagoTipoVisistante(models.Model):
    tipo_visitante = models.CharField(max_length=455, unique=True)

    class Meta:
        app_label = 'ecosistema'
        db_table = 'catalogo_tipo_visitante'
        ordering = ['-id']
    
    @classmethod
    def homologar_tipo_visitante(cls, tipo_visitante):
        try:
            catalogo = CatalagoTipoVisistante.objects.get(tipo_visitante=tipo_visitante)
            return catalogo.tipo_visitante
        except CatalagoTipoVisistante.DoesNotExist:
            return tipo_visitante


class CatalagoZAMuseos (models.Model):
    nombre = models.CharField(max_length=455)
    tipo = models.CharField(max_length=455)

    class Meta:
        app_label = 'ecosistema'
        db_table = "catalogo_za_museos"
        ordering = ['-id']

class CatalogoEntidad(models.Model):
    entidad = models.CharField(max_length=455, unique=True)

    class Meta:
        app_label = 'ecosistema'
        db_table = 'catalogo_entidades'
        ordering = ['-id']

        
class CatalogoAeropuertos(models.Model):
    aereopuerto = models.CharField(max_length=455, unique=True)
    entidad = models.CharField(max_length=455)

    class Meta:
        app_label = 'ecosistema'
        db_table = 'catalogo_aeropuertos'
        ordering = ['-id']


class Airbnb (models.Model):
    fecha_inicio = models.DateField(verbose_name='Fecha de inicio')
    fecha_fin = models.DateField(verbose_name='Fecha de fin')
    destino = models.CharField(max_length=455, null=True, blank=True, verbose_name='Destino')
    propiedad_renta = models.FloatField(verbose_name='Propiedad de renta')
    porcentaje_ocupacion = models.FloatField(verbose_name='Porcentaje de ocupación')
    tarifa_promedio = models.FloatField(verbose_name='Tarifa promedio')

    class Meta:
        app_label = 'ecosistema'
        db_table = "airbnb"
        ordering = ['-id']

class inversion_privada (models.Model):
    fecha = models.DateField()
    monto_ejecutado = models.FloatField()
    avance_proyecto = models.FloatField()
    observaciones = models.CharField(max_length=455)
    nombre_del_proyecto = models.CharField(max_length=455)
    id_del_proyecto = models.CharField(max_length=455)
    destino = models.CharField(max_length=455, null=True, blank=True)

    class Meta:
        app_label = 'ecosistema'
        db_table = "inversion_privada"
        ordering = ['-id']


class Certificacion(models.Model):
    fecha = models.DateField()
    destino = models.CharField(max_length=455, null=True, blank=True)
    tipo_de_certificacion = models.CharField(max_length=455)
    empresas_certificadas = models.IntegerField()

    class Meta:
        app_label = 'ecosistema'
        db_table = "certificacion"
        ordering = ['-id']

class empleo (models.Model):
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    hombres_empleados_gto = models.IntegerField(null=True, default=None)
    mujeres_empleadas_gto = models.IntegerField(null=True, default=None)
    hombres_empleados_sec_72_gto = models.IntegerField(null=True, default=None)
    mujeres_empleadas_sec_72_gto = models.IntegerField(null=True, default=None)
    hombres_empleados_sec_72_nac = models.IntegerField(null=True, default=None)
    mujeres_empleadas_sec_72_nac = models.IntegerField(null=True, default=None)

    class Meta:
        app_label = 'ecosistema'
        db_table = "empleo"
        ordering = ['-id']

class ModeloGD (models.Model):
    anio = models.IntegerField()
    destino = models.CharField(max_length=455, null=True, blank=True)
    tipo_de_visitante = models.CharField(max_length=455 , null=True, blank=True)
    gasto_diario_promedio = models.FloatField()
    participacion = models.FloatField()
    estadia_promedio = models.FloatField()



class Discapacidad(models.Model):
    destino = models.CharField(max_length=256)
    fecha = models.DateField()
    giro_comercial = models.CharField(max_length=256)
    empleos_fijos_h = models.BigIntegerField()
    empleos_fijos_m = models.BigIntegerField()
    empleos_temporales_h = models.BigIntegerField()
    empleos_temporales_m = models.BigIntegerField()
    empleados_discapacidad_h = models.BigIntegerField()
    empleados_discapacidad_m = models.BigIntegerField()

    class Meta:
        app_label = 'ecosistema'
        db_table = "empleo_discapacidad"
        ordering = ['-id']

class ParticipacionSegmentos(models.Model):
    ano = models.IntegerField()
    destino = models.CharField(max_length=256)
    segmento = models.CharField(max_length=256)
    participacion = models.FloatField()

    class Meta:
        app_label = 'ecosistema'
        db_table = "participacion_segmentos"
        ordering = ['-id']

class ParticipacionOrigen(models.Model):
    ano = models.IntegerField(verbose_name='Año')
    destino = models.CharField(max_length=256, verbose_name='Destino')
    part_visitantes_int = models.FloatField(verbose_name='Participación de Visitantes Internacionales')
    part_visitantes_nac = models.FloatField(verbose_name='Participación de Visitantes Nacionales')
    part_visitantes_est = models.FloatField(verbose_name='Participación de Visitantes Estatales')

    class Meta:
        app_label = 'ecosistema'
        db_table = "participacion_origen"
        ordering = ['-id']

class FuenteInfoPerfilVisitanteEvento(models.Model):
    ano = models.IntegerField()
    folio = models.IntegerField()
    fecha = models.DateField()
    destino = models.CharField(max_length=256)
    nombre_evento = models.CharField(max_length=256)
    segmento = models.CharField(max_length=256)
    tipo_participante = models.CharField(max_length=256)
    residencia = models.CharField(max_length=256)
    tipo_asistente = models.CharField(max_length=256)
    municipio = models.CharField(max_length=256)
    estado = models.CharField(max_length=256)
    pais = models.CharField(max_length=256)
    origen = models.CharField(max_length=256)
    tipo_hospedaje = models.CharField(max_length=256)
    tipo_visitante = models.CharField(max_length=256)
    grupo_viaje = models.CharField(max_length=256)
    acompanantes_maxmin = models.FloatField()
    nps_evento = models.FloatField()
    nps_evento_categoria = models.CharField(max_length=256)
    edad = models.IntegerField()
    nse = models.CharField(max_length=256)
    sexo = models.CharField(max_length=256)
    codigo_encuesta_ano = models.CharField(max_length=256)

    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        app_label = 'ecosistema'
        db_table = "perfil_visitante_eventos"
        ordering = ['-id']

class FuenteInfoPerfilVisitanteDestino(models.Model):
    ano = models.IntegerField(verbose_name='Año')
    folio = models.IntegerField(verbose_name='Folio')
    herramienta = models.CharField(max_length=256, verbose_name='Herramienta')
    fecha = models.DateField(verbose_name='Fecha')
    temporada = models.CharField(max_length=256, verbose_name='Temporada')
    destino = models.CharField(max_length=256, verbose_name='Destino')
    residencia = models.CharField(max_length=256, verbose_name='Residencia')
    tipo_asistente = models.CharField(max_length=256, verbose_name='Tipo de asistente')
    municipio = models.CharField(max_length=256, verbose_name='Municipio')
    estado = models.CharField(max_length=256, verbose_name='Estado')
    pais = models.CharField(max_length=256, verbose_name='País')
    origen = models.CharField(max_length=256, verbose_name='Origen')
    motivo_visita = models.CharField(max_length=256, verbose_name='Motivo de visita')
    motivo_visita_otro = models.CharField(max_length=256, verbose_name='Otro motivo de visita')
    segmento = models.CharField(max_length=256, verbose_name='Segmento')
    tipo_hospedaje = models.CharField(max_length=256, verbose_name='Tipo de hospedaje')
    tipo_visitante = models.CharField(max_length=256, verbose_name='Tipo de visitante')
    estadia_dias = models.FloatField(verbose_name='Estadía en días')
    estadia_hrs = models.FloatField(verbose_name='Estadía en horas')
    acompanantes = models.FloatField(verbose_name='Acompañantes')
    acompanantes_maxmin = models.FloatField(verbose_name='Acompañantes (máx/min)')
    medio_transporte_edo = models.CharField(max_length=256, verbose_name='Medio de transporte desde el estado')
    tiene_fam = models.CharField(max_length=256, verbose_name='¿Tiene familiares en el destino?')
    visita_fam = models.CharField(max_length=256, verbose_name='Motivo de visita a familiares')
    sat_hospedaje = models.IntegerField(verbose_name='Satisfacción con el hospedaje')
    sat_ayb = models.IntegerField(verbose_name='Satisfacción con alimentos y bebidas')
    sat_atractivos = models.IntegerField(verbose_name='Satisfacción con atractivos turísticos')
    sat_tours = models.IntegerField(verbose_name='Satisfacción con tours o actividades')
    sat_central = models.IntegerField(verbose_name='Satisfacción con la central de autobuses')
    sat_aeropuerto = models.IntegerField(verbose_name='Satisfacción con el aeropuerto')
    sat_carretera = models.IntegerField(verbose_name='Satisfacción con carreteras')
    sat_infotur = models.IntegerField(verbose_name='Satisfacción con módulos de información turística')
    sat_estacionamiento = models.IntegerField(verbose_name='Satisfacción con estacionamientos')
    sat_hospitalidad = models.IntegerField(verbose_name='Satisfacción con la hospitalidad')
    sat_seguridad = models.IntegerField(verbose_name='Satisfacción con la seguridad')
    sat_experiencia = models.IntegerField(verbose_name='Satisfacción con la experiencia general')
    sat_accesibilidad = models.IntegerField(verbose_name='Satisfacción con la accesibilidad')
    sat_senaletica = models.IntegerField(verbose_name='Satisfacción con señalética')
    sat_transporte = models.IntegerField(verbose_name='Satisfacción con transporte público')
    sat_limpieza = models.IntegerField(verbose_name='Satisfacción con la limpieza')
    sat_eventos = models.IntegerField(verbose_name='Satisfacción con eventos y espectáculos')
    sat_protocolos = models.IntegerField(verbose_name='Satisfacción con protocolos COVID-19')
    sat_precios = models.IntegerField(verbose_name='Satisfacción con precios')
    recomendacion_destino = models.CharField(max_length=256, verbose_name='Recomendación del destino')
    retorno_destino = models.CharField(max_length=256, verbose_name='Retorno al destino')
    nps_destino = models.FloatField(verbose_name='NPS del destino')
    nps_destino_categoria = models.CharField(max_length=256, verbose_name='Categoría NPS del destino')
    nps_hotel = models.FloatField(verbose_name='NPS del hotel')
    nps_ayb = models.FloatField(verbose_name='NPS de alimentos y bebidas')
    nps_atractivos = models.FloatField(verbose_name='NPS de atractivos turísticos')
    nps_tours = models.FloatField(verbose_name='NPS de tours o actividades')
    vio_escucho_noticias = models.CharField(max_length=256, verbose_name='Vio o escuchó noticias del destino')
    impacto_noticias = models.CharField(max_length=256, verbose_name='Impacto de las noticias en la visita')
    identifico_practicas_sust = models.CharField(max_length=256, verbose_name='Identificación de prácticas sustentables')
    edad = models.FloatField(verbose_name='Edad')
    nse = models.CharField(max_length=256, verbose_name='NSE (Nivel Socioeconómico)')
    sexo = models.CharField(max_length=256, verbose_name='Sexo')
    proposito_visita_destino_estado = models.CharField(max_length=256, verbose_name='Propósito de la visita al destino o estado')
    codigo_encuesta_ano = models.CharField(max_length=256, verbose_name='Código de encuesta del año')

    def toJSON(self):
        item = model_to_dict(self)
        return item


    class Meta:
        app_label = 'ecosistema'
        db_table = "perfil_visitante_destinos"
        ordering = ['-id']



class FuenteInfoEntornoN(models.Model):
    entidad = models.CharField(max_length=256, verbose_name='Entidad')
    fecha = models.DateField(verbose_name='Fecha')
    cuartos_disponibles_promedio = models.FloatField(verbose_name='Cuartos Disponibles Promedio')
    cuartos_disponibles = models.FloatField(verbose_name='Cuartos Disponibles')
    cuartos_ocupados = models.FloatField(verbose_name='Cuartos Ocupados')
    cuartos_ocupados_nacionales = models.FloatField(verbose_name='Cuartos Ocupados Nacionales')
    cuartos_ocupados_extranjeros = models.FloatField(verbose_name='Cuartos Ocupados Extranjeros')
    cuartos_ocupados_sin_clasificar = models.FloatField(verbose_name='Cuartos Ocupados Sin Clasificar')
    llegada_de_turistas = models.IntegerField(verbose_name='Llegada de Turistas')
    llegada_de_turistas_nacionales = models.FloatField(verbose_name='Llegada de Turistas Nacionales')
    llegada_de_turistas_extranjeros = models.FloatField(verbose_name='Llegada de Turistas Extranjeros')
    turistas_noche = models.FloatField(verbose_name='Turistas Noche')
    turistas_noche_nacionales = models.FloatField(verbose_name='Turistas Noche Nacionales')
    turistas_noche_extranjeros = models.FloatField(verbose_name='Turistas Noche Extranjeros')
    porcentaje_de_ocupacion = models.FloatField(verbose_name='Porcentaje de Ocupación')
    porcentaje_de_ocupacion_nacionales = models.FloatField(verbose_name='Porcentaje de Ocupación Nacionales')
    porcentaje_de_ocupacion_extranjeros = models.FloatField(verbose_name='Porcentaje de Ocupación Extranjeros')
    porcentaje_de_ocupacion_sin_clasificar = models.IntegerField(verbose_name='Porcentaje de Ocupación Sin Clasificar')
    densidad = models.FloatField(verbose_name='Densidad')
    densidad_nacionales = models.FloatField(verbose_name='Densidad Nacionales')
    densidad_extranjeros = models.FloatField(verbose_name='Densidad Extranjeros')
    estadia_promedio = models.FloatField(verbose_name='Estadía Promedio')
    estadia_promedio_nacionales = models.FloatField(verbose_name='Estadía Promedio Nacionales')
    estadia_promedio_extranjeros = models.FloatField(verbose_name='Estadía Promedio Extranjeros')
    
    def toJSON(self):
        item = model_to_dict(self)
        return item
    
    class Meta:
        app_label = 'ecosistema'
        db_table = "entorno_nacional"
        ordering = ['-id']





class Aeropuerto(models.Model):
    fecha = models.DateField()
    pasajeros_aeropuerto_gto = models.FloatField()
    pasajeros_nacionales = models.FloatField()
    pasajeros_internacionales = models.FloatField()

    vuelos = models.FloatField()

    class Meta:
        app_label = 'ecosistema'
        db_table = "pasajeros_aeropuerto"
        ordering = ['-id']

class Aerolinea(models.Model):
    fecha = models.DateField()
    destino_aeropuerto = models.CharField(max_length=256)
    destino_aeropuerto_id = models.CharField(max_length=256)
    tipo_aerolinea = models.CharField(max_length=256)
    codigo_aerolinea = models.CharField(max_length=256)

    class Meta:
        app_label = 'ecosistema'
        db_table = "aerolineas_destino"
        ordering = ['-id']

class InventarioTuristico(models.Model):
    ano = models.IntegerField()
    giro = models.CharField(max_length=256)
    destino = models.CharField(max_length=256)
    inventario = models.IntegerField()

    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        app_label = 'ecosistema'
        db_table = "inventario_turistico"
        ordering = ['-id']

class DirectorioHotelero(models.Model):
    id_establecimiento = models.IntegerField()
    nombre_de_la_unidad_economica = models.CharField(max_length=256)
    razon_social = models.CharField(max_length=256)
    codigo_de_la_clase_de_actividad_scian = models.IntegerField()
    nombre_de_clase_de_la_actividad = models.CharField(max_length=256)
    descripcion_estrato_personal_ocupado = models.CharField(max_length=256)
    tipo_de_vialidad = models.CharField(max_length=256)
    nombre_de_la_vialidad = models.CharField(max_length=256)
    tipo_de_entre_vialidad_1 = models.CharField(max_length=256)
    nombre_de_entre_vialidad_1 = models.CharField(max_length=256)
    tipo_de_entre_vialidad_2 = models.CharField(max_length=256)
    nombre_de_entre_vialidad_2 = models.CharField(max_length=256)
    tipo_de_entre_vialidad_3 = models.CharField(max_length=256)
    nombre_de_entre_vialidad_3 = models.CharField(max_length=256)
    numero_exterior_o_kilometro = models.CharField(max_length=256)
    letra_exterior = models.CharField(max_length=256)
    edificio = models.CharField(max_length=256)
    edificio_piso = models.DecimalField(max_digits=10, decimal_places=2)
    numero_interior = models.DecimalField(max_digits=10, decimal_places=2)
    letra_interior = models.CharField(max_length=256)
    tipo_de_asentamiento_humano = models.CharField(max_length=256)
    nombre_de_asentamiento_humano = models.CharField(max_length=256)
    tipo_centro_comercial = models.CharField(max_length=256)
    c_industrial_comercial_o_mercado = models.CharField(max_length=256)
    numero_de_local = models.DecimalField(max_digits=10, decimal_places=2)
    codigo_postal = models.CharField(max_length=256)
    clave_entidad = models.IntegerField()
    entidad_federativa = models.CharField(max_length=256)
    clave_municipio = models.DecimalField(max_digits=10, decimal_places=2)
    municipio = models.CharField(max_length=256)
    clave_localidad = models.DecimalField(max_digits=10, decimal_places=2)
    localidad = models.CharField(max_length=256)
    area_geoestadistica_basica = models.CharField(max_length=256)
    manzana = models.DecimalField(max_digits=10, decimal_places=2)
    numero_de_telefono = models.CharField(max_length=256)
    correo_electronico = models.CharField(max_length=256)
    sitio_en_internet = models.CharField(max_length=256)
    tipo_de_establecimiento = models.CharField(max_length=256)
    latitud = models.DecimalField(max_digits=10, decimal_places=7)
    longitud = models.DecimalField(max_digits=10, decimal_places=7)
    fecha_de_incorporacion_al_denue = models.DateField()
    categoria_turistica = models.CharField(max_length=256)
    no_cuartos = models.IntegerField()
    unidades = models.DecimalField(max_digits=10, decimal_places=2)
    espacios_cajones = models.DecimalField(max_digits=10, decimal_places=2)
    no_camas = models.DecimalField(max_digits=10, decimal_places=2)
    cadena = models.DecimalField(max_digits=10, decimal_places=2)
    operadora = models.DecimalField(max_digits=10, decimal_places=2)
    responsable = models.CharField(max_length=256)
    cargo = models.CharField(max_length=256)
    imss = models.DecimalField(max_digits=10, decimal_places=2)
    inicio_de_operaciones_este_ano = models.CharField(max_length=256)
    fecha_de_inicio_de_operaciones = models.DateField()
    centro_turistico = models.CharField(max_length=256)
    zona = models.CharField(max_length=256)
    datatur = models.CharField(max_length=256)
    hotel_boutique = models.DecimalField(max_digits=10, decimal_places=2)
    nombre_de_la_cadena = models.CharField(max_length=256)
    hoteles_tesoros = models.CharField(max_length=256)

    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        app_label = 'ecosistema'
        db_table = "directorio_hotelero"
        ordering = ['-id']

#Direcctorio Turistico
class DirectorioAgenciasDeViajes(models.Model):
    giro = models.CharField(max_length=256, verbose_name='Giro')
    clave_del_giro = models.IntegerField(verbose_name='Clave del Giro')
    entidad = models.CharField(max_length=256, verbose_name='Entidad')
    clave_entidad = models.IntegerField(verbose_name='Clave de Entidad')
    destino = models.CharField(max_length=256, verbose_name='Destino')
    clave_municipio = models.IntegerField(verbose_name='Clave de Municipio')
    nombre_comercial = models.CharField(max_length=256, verbose_name='Nombre Comercial')
    razon_social = models.CharField(max_length=256, verbose_name='Razón Social')
    rfc = models.CharField(max_length=256, verbose_name='RFC')
    calle = models.CharField(max_length=256, verbose_name='Calle')
    numero = models.CharField(max_length=256, verbose_name='Número')
    colonia = models.CharField(max_length=256, verbose_name='Colonia')
    codigo_postal = models.IntegerField(verbose_name='Código Postal')
    lada = models.IntegerField(verbose_name='Lada')
    telefono_1 = models.CharField(max_length=256, verbose_name='Teléfono 1')
    telefono_2 = models.CharField(max_length=256, verbose_name='Teléfono 2')
    celular = models.CharField(max_length=256, verbose_name='Celular')
    correo_electronico = models.EmailField(max_length=256, verbose_name='Correo Electrónico')
    sitio_web = models.URLField(max_length=256, verbose_name='Sitio Web')
    ret = models.CharField(max_length=256, verbose_name='RET')
    rnt = models.CharField(max_length=256, verbose_name='RNT')

    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        app_label = 'ecosistema'
        db_table = "directorio_agencias_de_viajes"
        ordering = ['-id']

class DirectorioAlimentosYBebidas(models.Model):
    giro = models.CharField(max_length=256, verbose_name='Giro')
    clave_del_giro = models.IntegerField(verbose_name='Clave del Giro')
    entidad = models.CharField(max_length=256, verbose_name='Entidad')
    clave_entidad = models.IntegerField(verbose_name='Clave de Entidad')
    destino = models.CharField(max_length=256, verbose_name='Destino')
    clave_municipio = models.IntegerField(verbose_name='Clave de Municipio')
    nombre_comercial = models.CharField(max_length=256, verbose_name='Nombre Comercial')
    razon_social = models.CharField(max_length=256, verbose_name='Razón Social')
    rfc = models.CharField(max_length=256, verbose_name='RFC')
    calle = models.CharField(max_length=256, verbose_name='Calle')
    numero = models.CharField(max_length=256, verbose_name='Número')
    colonia = models.CharField(max_length=256, verbose_name='Colonia')
    codigo_postal = models.IntegerField(verbose_name='Código Postal')
    lada = models.IntegerField(verbose_name='Lada')
    telefono_1 = models.CharField(max_length=256, verbose_name='Teléfono 1')
    telefono_2 = models.CharField(max_length=256, verbose_name='Teléfono 2')
    celular = models.CharField(max_length=256, verbose_name='Celular')
    correo_electronico = models.EmailField(max_length=256, verbose_name='Correo Electrónico')
    sitio_web = models.URLField(max_length=256, verbose_name='Sitio Web')
    ret = models.CharField(max_length=256, verbose_name='RET')
    rnt = models.CharField(max_length=256, verbose_name='RNT')

    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        app_label = 'ecosistema'
        db_table = "directorio_alimentos_y_bebidas"
        ordering = ['-id']

class DirectorioArrendadoras(models.Model):
    giro = models.CharField(max_length=256, verbose_name='Giro')
    clave_del_giro = models.IntegerField(verbose_name='Clave del Giro')
    entidad = models.CharField(max_length=256, verbose_name='Entidad')
    clave_entidad = models.IntegerField(verbose_name='Clave de Entidad')
    destino = models.CharField(max_length=256, verbose_name='Destino')
    clave_municipio = models.IntegerField(verbose_name='Clave de Municipio')
    nombre_comercial = models.CharField(max_length=256, verbose_name='Nombre Comercial')
    razon_social = models.CharField(max_length=256, verbose_name='Razón Social')
    rfc = models.CharField(max_length=256, verbose_name='RFC')
    calle = models.CharField(max_length=256, verbose_name='Calle')
    numero = models.CharField(max_length=256, verbose_name='Número')
    colonia = models.CharField(max_length=256, verbose_name='Colonia')
    codigo_postal = models.IntegerField(verbose_name='Código Postal')
    lada = models.IntegerField(verbose_name='Lada')
    telefono_1 = models.CharField(max_length=256, verbose_name='Teléfono 1')
    telefono_2 = models.CharField(max_length=256, verbose_name='Teléfono 2')
    celular = models.CharField(max_length=256, verbose_name='Celular')
    correo_electronico = models.EmailField(max_length=256, verbose_name='Correo Electrónico')
    sitio_web = models.URLField(max_length=256, verbose_name='Sitio Web')
    ret = models.CharField(max_length=256, verbose_name='RET')
    rnt = models.CharField(max_length=256, verbose_name='RNT')

    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        app_label = 'ecosistema'
        db_table = "directorio_arrendadoras"
        ordering = ['-id']

class DirectorioActivosRecreacionYDeporte(models.Model):
    giro = models.CharField(max_length=256, verbose_name='Giro')
    clave_del_giro = models.IntegerField(verbose_name='Clave del Giro')
    entidad = models.CharField(max_length=256, verbose_name='Entidad')
    clave_entidad = models.IntegerField(verbose_name='Clave de Entidad')
    destino = models.CharField(max_length=256, verbose_name='Destino')
    clave_municipio = models.IntegerField(verbose_name='Clave de Municipio')
    nombre_comercial = models.CharField(max_length=256, verbose_name='Nombre Comercial')
    razon_social = models.CharField(max_length=256, verbose_name='Razón Social')
    rfc = models.CharField(max_length=256, verbose_name='RFC')
    calle = models.CharField(max_length=256, verbose_name='Calle')
    numero = models.CharField(max_length=256, verbose_name='Número')
    colonia = models.CharField(max_length=256, verbose_name='Colonia')
    codigo_postal = models.IntegerField(verbose_name='Código Postal')
    lada = models.IntegerField(verbose_name='Lada')
    telefono_1 = models.CharField(max_length=256, verbose_name='Teléfono 1')
    telefono_2 = models.CharField(max_length=256, verbose_name='Teléfono 2')
    celular = models.CharField(max_length=256, verbose_name='Celular')
    correo_electronico = models.EmailField(max_length=256, verbose_name='Correo Electrónico')
    sitio_web = models.URLField(max_length=256, verbose_name='Sitio Web')
    ret = models.CharField(max_length=256, verbose_name='RET')
    rnt = models.CharField(max_length=256, verbose_name='RNT')

    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        app_label = 'ecosistema'
        db_table = "directorio_atractivos_recreacion_y_deporte"
        ordering = ['-id']

class DirectorioAuxilioTuristico(models.Model):
    giro = models.CharField(max_length=256, verbose_name='Giro')
    clave_del_giro = models.IntegerField(verbose_name='Clave del Giro')
    entidad = models.CharField(max_length=256, verbose_name='Entidad')
    clave_entidad = models.IntegerField(verbose_name='Clave de Entidad')
    destino = models.CharField(max_length=256, verbose_name='Destino')
    clave_municipio = models.IntegerField(verbose_name='Clave de Municipio')
    nombre_comercial = models.CharField(max_length=256, verbose_name='Nombre Comercial')
    razon_social = models.CharField(max_length=256, verbose_name='Razón Social')
    rfc = models.CharField(max_length=256, verbose_name='RFC')
    calle = models.CharField(max_length=256, verbose_name='Calle')
    numero = models.CharField(max_length=256, verbose_name='Número')
    colonia = models.CharField(max_length=256, verbose_name='Colonia')
    codigo_postal = models.IntegerField(verbose_name='Código Postal')
    lada = models.IntegerField(verbose_name='Lada')
    telefono_1 = models.CharField(max_length=256, verbose_name='Teléfono 1')
    telefono_2 = models.CharField(max_length=256, verbose_name='Teléfono 2')
    celular = models.CharField(max_length=256, verbose_name='Celular')
    correo_electronico = models.EmailField(max_length=256, verbose_name='Correo Electrónico')
    sitio_web = models.URLField(max_length=256, verbose_name='Sitio Web')
    ret = models.CharField(max_length=256, verbose_name='RET')
    rnt = models.CharField(max_length=256, verbose_name='RNT')

    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        app_label = 'ecosistema'
        db_table = "directorio_auxilio_turistico"
        ordering = ['-id']

class DirectorioBalneariosParquesAcuaticos(models.Model):
    giro = models.CharField(max_length=256, verbose_name='Giro')
    clave_del_giro = models.IntegerField(verbose_name='Clave del Giro')
    entidad = models.CharField(max_length=256, verbose_name='Entidad')
    clave_entidad = models.IntegerField(verbose_name='Clave de Entidad')
    destino = models.CharField(max_length=256, verbose_name='Destino')
    clave_municipio = models.IntegerField(verbose_name='Clave de Municipio')
    nombre_comercial = models.CharField(max_length=256, verbose_name='Nombre Comercial')
    razon_social = models.CharField(max_length=256, verbose_name='Razón Social')
    rfc = models.CharField(max_length=256, verbose_name='RFC')
    calle = models.CharField(max_length=256, verbose_name='Calle')
    numero = models.CharField(max_length=256, verbose_name='Número')
    colonia = models.CharField(max_length=256, verbose_name='Colonia')
    codigo_postal = models.IntegerField(verbose_name='Código Postal')
    lada = models.IntegerField(verbose_name='Lada')
    telefono_1 = models.CharField(max_length=256, verbose_name='Teléfono 1')
    telefono_2 = models.CharField(max_length=256, verbose_name='Teléfono 2')
    celular = models.CharField(max_length=256, verbose_name='Celular')
    correo_electronico = models.EmailField(max_length=256, verbose_name='Correo Electrónico')
    sitio_web = models.URLField(max_length=256, verbose_name='Sitio Web')
    ret = models.CharField(max_length=256, verbose_name='RET')
    rnt = models.CharField(max_length=256, verbose_name='RNT')
    numero_albercas = models.IntegerField(verbose_name='Número de Albercas')
    numero_toboganes = models.IntegerField(verbose_name='Número de Toboganes')
    aguas_termales = models.CharField(max_length=256, verbose_name='Aguas Termales')

    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        app_label = 'ecosistema'
        db_table = "directorio_balnearios_parques_acuaticos"
        ordering = ['-id']

class DirectorioCampoDeGolf(models.Model):
    giro = models.CharField(max_length=256, verbose_name='Giro')
    clave_del_giro = models.IntegerField(verbose_name='Clave del Giro')
    entidad = models.CharField(max_length=256, verbose_name='Entidad')
    clave_entidad = models.IntegerField(verbose_name='Clave de Entidad')
    destino = models.CharField(max_length=256, verbose_name='Destino')
    clave_municipio = models.IntegerField(verbose_name='Clave de Municipio')
    nombre_comercial = models.CharField(max_length=256, verbose_name='Nombre Comercial')
    razon_social = models.CharField(max_length=256, verbose_name='Razón Social')
    rfc = models.CharField(max_length=256, verbose_name='RFC')
    calle = models.CharField(max_length=256, verbose_name='Calle')
    numero = models.CharField(max_length=256, verbose_name='Número')
    colonia = models.CharField(max_length=256, verbose_name='Colonia')
    codigo_postal = models.IntegerField(verbose_name='Código Postal')
    lada = models.IntegerField(verbose_name='Lada')
    telefono_1 = models.CharField(max_length=256, verbose_name='Teléfono 1')
    telefono_2 = models.CharField(max_length=256, verbose_name='Teléfono 2')
    celular = models.CharField(max_length=256, verbose_name='Celular')
    correo_electronico = models.EmailField(max_length=256, verbose_name='Correo Electrónico')
    sitio_web = models.URLField(max_length=256, verbose_name='Sitio Web')
    ret = models.CharField(max_length=256, verbose_name='RET')
    rnt = models.CharField(max_length=256, verbose_name='RNT')

    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        app_label = 'ecosistema'
        db_table = "directorio_campo_de_golf"
        ordering = ['-id']

class DirectorioCapacitacionTuristica(models.Model):
    giro = models.CharField(max_length=256, verbose_name='Giro')
    clave_del_giro = models.IntegerField(verbose_name='Clave del Giro')
    entidad = models.CharField(max_length=256, verbose_name='Entidad')
    clave_entidad = models.IntegerField(verbose_name='Clave de Entidad')
    destino = models.CharField(max_length=256, verbose_name='Destino')
    clave_municipio = models.IntegerField(verbose_name='Clave de Municipio')
    nombre_comercial = models.CharField(max_length=256, verbose_name='Nombre Comercial')
    razon_social = models.CharField(max_length=256, verbose_name='Razón Social')
    rfc = models.CharField(max_length=256, verbose_name='RFC')
    calle = models.CharField(max_length=256, verbose_name='Calle')
    numero = models.CharField(max_length=256, verbose_name='Número')
    colonia = models.CharField(max_length=256, verbose_name='Colonia')
    codigo_postal = models.IntegerField(verbose_name='Código Postal')
    lada = models.IntegerField(verbose_name='Lada')
    telefono_1 = models.CharField(max_length=256, verbose_name='Teléfono 1')
    telefono_2 = models.CharField(max_length=256, verbose_name='Teléfono 2')
    celular = models.CharField(max_length=256, verbose_name='Celular')
    correo_electronico = models.EmailField(max_length=256, verbose_name='Correo Electrónico')
    sitio_web = models.URLField(max_length=256, verbose_name='Sitio Web')
    ret = models.CharField(max_length=256, verbose_name='RET')
    tipo = models.CharField(max_length=256, verbose_name='Tipo')
    lic_gastronomia = models.CharField(max_length=256, verbose_name='Licencia de Gastronomía')
    lic_turismo = models.CharField(max_length=256, verbose_name='Licencia de Turismo')
    posgrado_en_turismo = models.CharField(max_length=256, verbose_name='Posgrado en Turismo')
    certificacion_como_guia_de_turista = models.CharField(max_length=256, verbose_name='Certificación como Guía de Turista')
    otros_estudios_en_turismo = models.CharField(max_length=256, verbose_name='Otros Estudios en Turismo')
    rnt = models.CharField(max_length=256, verbose_name='RNT')

    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        app_label = 'ecosistema'
        db_table = "directorio_capacitacion_turistica"
        ordering = ['-id']

class DirectorioGuiasDeTuristas(models.Model):
    giro = models.CharField(max_length=256, verbose_name='Giro')
    clave_del_giro = models.IntegerField(verbose_name='Clave del Giro')
    entidad = models.CharField(max_length=256, verbose_name='Entidad')
    clave_entidad = models.IntegerField(verbose_name='Clave de Entidad')
    destino = models.CharField(max_length=256, verbose_name='Destino')
    clave_municipio = models.IntegerField(verbose_name='Clave de Municipio')
    nombre_comercial = models.CharField(max_length=256, verbose_name='Nombre Comercial')
    razon_social = models.CharField(max_length=256, verbose_name='Razón Social')
    rfc = models.CharField(max_length=256, verbose_name='RFC')
    calle = models.CharField(max_length=256, verbose_name='Calle')
    numero = models.CharField(max_length=256, verbose_name='Número')
    colonia = models.CharField(max_length=256, verbose_name='Colonia')
    codigo_postal = models.IntegerField(verbose_name='Código Postal')
    lada = models.IntegerField(verbose_name='Lada')
    telefono_1 = models.CharField(max_length=256, verbose_name='Teléfono 1')
    telefono_2 = models.CharField(max_length=256, verbose_name='Teléfono 2')
    celular = models.CharField(max_length=256, verbose_name='Celular')
    correo_electronico = models.EmailField(max_length=256, verbose_name='Correo Electrónico')
    sitio_web = models.URLField(max_length=256, verbose_name='Sitio Web')
    ret = models.CharField(max_length=256, verbose_name='RET')
    rnt = models.CharField(max_length=256, verbose_name='RNT')
    tipo = models.CharField(max_length=256, verbose_name='Tipo')
    no_acreditacion = models.CharField(max_length=256, verbose_name='Número de Acreditación')
    vigencia_acreditacion = models.FloatField(verbose_name='Vigencia de Acreditación')
    especialidad = models.CharField(max_length=256, verbose_name='Especialidad')

    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        app_label = 'ecosistema'
        db_table = "directorio_guias_de_turistas"
        ordering = ['-id']
        
class DirectorioOperadores(models.Model):
    giro = models.CharField(max_length=256, verbose_name='Giro')
    clave_del_giro = models.IntegerField(verbose_name='Clave del Giro')
    entidad = models.CharField(max_length=256, verbose_name='Entidad')
    clave_entidad = models.IntegerField(verbose_name='Clave de Entidad')
    destino = models.CharField(max_length=256, verbose_name='Destino')
    clave_municipio = models.IntegerField(verbose_name='Clave de Municipio')
    nombre_comercial = models.CharField(max_length=256, verbose_name='Nombre Comercial')
    razon_social = models.CharField(max_length=256, verbose_name='Razón Social')
    rfc = models.CharField(max_length=256, verbose_name='RFC')
    calle = models.CharField(max_length=256, verbose_name='Calle')
    numero = models.CharField(max_length=256, verbose_name='Número')
    colonia = models.CharField(max_length=256, verbose_name='Colonia')
    codigo_postal = models.IntegerField(verbose_name='Código Postal')
    lada = models.IntegerField(verbose_name='Lada')
    telefono_1 = models.CharField(max_length=256, verbose_name='Teléfono 1')
    telefono_2 = models.CharField(max_length=256, verbose_name='Teléfono 2')
    celular = models.CharField(max_length=256, verbose_name='Celular')
    correo_electronico = models.EmailField(max_length=256, verbose_name='Correo Electrónico')
    sitio_web = models.URLField(max_length=256, verbose_name='Sitio Web')
    ret = models.CharField(max_length=256, verbose_name='RET')
    rnt = models.CharField(max_length=256, verbose_name='RNT')

    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        app_label = 'ecosistema'
        db_table = "directorio_operadores"
        ordering = ['-id']
        
class DirectorioProductosTuristicos(models.Model):
    giro = models.CharField(max_length=256, verbose_name='Giro')
    clave_del_giro = models.IntegerField(verbose_name='Clave del Giro')
    entidad = models.CharField(max_length=256, verbose_name='Entidad')
    clave_entidad = models.IntegerField(verbose_name='Clave de Entidad')
    destino = models.CharField(max_length=256, verbose_name='Destino')
    nombre_comercial = models.CharField(max_length=256, verbose_name='Nombre Comercial')
    razon_social = models.CharField(max_length=256, verbose_name='Razón Social')
    rfc = models.CharField(max_length=256, verbose_name='RFC')
    calle = models.CharField(max_length=256, verbose_name='Calle')
    numero = models.IntegerField(max_length=256, verbose_name='Número')
    colonia = models.CharField(max_length=256, verbose_name='Colonia')
    codigo_postal = models.IntegerField(verbose_name='Código Postal')
    lada = models.IntegerField(verbose_name='Lada')
    telefono_1 = models.CharField(max_length=256, verbose_name='Teléfono 1')
    telefono_2 = models.CharField(max_length=256, verbose_name='Teléfono 2')
    celular = models.CharField(max_length=256, verbose_name='Celular')
    correo_electronico = models.EmailField(max_length=256, verbose_name='Correo Electrónico')
    sitio_web = models.URLField(max_length=656, verbose_name='Sitio Web')
    ret = models.CharField(max_length=256, verbose_name='RET')
    rnt = models.CharField(max_length=256, verbose_name='RNT')
    segmento = models.CharField(max_length=256, verbose_name='Segmento')
    clave_municipio = models.IntegerField(verbose_name='Clave de Municipio')

    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        app_label = 'ecosistema'
        db_table = "directorio_productos_turisticos"
        ordering = ['-id']
        
class DirectorioRecintosAuditoriosYSalones(models.Model):
    giro = models.CharField(max_length=256, verbose_name='Giro')
    clave_del_giro = models.IntegerField(verbose_name='Clave del Giro')
    entidad = models.CharField(max_length=256, verbose_name='Entidad')
    clave_entidad = models.IntegerField(verbose_name='Clave de Entidad')
    destino = models.CharField(max_length=256, verbose_name='Destino')
    clave_municipio = models.IntegerField(verbose_name='Clave de Municipio')
    nombre_comercial = models.CharField(max_length=256, verbose_name='Nombre Comercial')
    razon_social = models.CharField(max_length=256, verbose_name='Razón Social')
    rfc = models.CharField(max_length=256, verbose_name='RFC')
    calle = models.CharField(max_length=256, verbose_name='Calle')
    numero = models.CharField(max_length=256, verbose_name='Número')
    colonia = models.CharField(max_length=256, verbose_name='Colonia')
    codigo_postal = models.IntegerField(verbose_name='Código Postal')
    lada = models.IntegerField(verbose_name='Lada')
    telefono_1 = models.CharField(max_length=256, verbose_name='Teléfono 1')
    telefono_2 = models.CharField(max_length=256, verbose_name='Teléfono 2')
    celular = models.CharField(max_length=256, verbose_name='Celular')
    correo_electronico = models.EmailField(max_length=256, verbose_name='Correo Electrónico')
    sitio_web = models.URLField(max_length=656, verbose_name='Sitio Web')
    ret = models.CharField(max_length=256, verbose_name='RET')
    rnt = models.CharField(max_length=256, verbose_name='RNT')
    modalidad = models.CharField(max_length=256, verbose_name='Modalidad')
    depende_de_hotel_o_restaurante = models.CharField(max_length=256, verbose_name='Depende de Hotel o Restaurante')
    no_de_salones = models.CharField(max_length=256, verbose_name='Número de Salones')
    capacidad_maxima = models.CharField(max_length=256, verbose_name='Capacidad Máxima')

    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        app_label = 'ecosistema'
        db_table = "directorio_recintos_auditorios_y_salones"
        ordering = ['-id']

class DirectorioSpa(models.Model):
    giro = models.CharField(max_length=256, verbose_name='Giro')
    clave_del_giro = models.IntegerField(verbose_name='Clave del Giro')
    entidad = models.CharField(max_length=256, verbose_name='Entidad')
    clave_entidad = models.IntegerField(verbose_name='Clave de Entidad')
    destino = models.CharField(max_length=256, verbose_name='Destino')
    clave_municipio = models.IntegerField(verbose_name='Clave de Municipio')
    nombre_comercial = models.CharField(max_length=256, verbose_name='Nombre Comercial')
    razon_social = models.CharField(max_length=256, verbose_name='Razón Social')
    rfc = models.CharField(max_length=256, verbose_name='RFC')
    calle = models.CharField(max_length=256, verbose_name='Calle')
    numero = models.CharField(max_length=256, verbose_name='Número')
    colonia = models.CharField(max_length=256, verbose_name='Colonia')
    codigo_postal = models.IntegerField(verbose_name='Código Postal')
    lada = models.IntegerField(verbose_name='Lada')
    telefono_1 = models.CharField(max_length=256, verbose_name='Teléfono 1')
    telefono_2 = models.CharField(max_length=256, verbose_name='Teléfono 2')
    celular = models.CharField(max_length=256, verbose_name='Celular')
    correo_electronico = models.EmailField(max_length=256, verbose_name='Correo Electrónico')
    sitio_web = models.URLField(max_length=656, verbose_name='Sitio Web')
    ret = models.CharField(max_length=256, verbose_name='RET')
    rnt = models.CharField(max_length=256, verbose_name='RNT')

    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        app_label = 'ecosistema'
        db_table = "directorio_spa"

class Pasajeros_Ent_Nac (models.Model):
    aereopuerto = models.CharField(max_length=256, verbose_name='Aeropuerto')
    entidad = models.CharField(max_length=256, verbose_name='Entidad')
    ano = models.IntegerField(verbose_name='Año')
    nacionales = models.IntegerField(verbose_name='Pasajeros Nacionales')
    internacionales = models.IntegerField(verbose_name='Pasajeros Internacionales')
    regulares = models.IntegerField(verbose_name='Pasajeros Regulares')
    nacionales_regulares = models.IntegerField(verbose_name='Pasajeros Nacionales Regulares')
    internacionales_regulares = models.IntegerField(verbose_name='Pasajeros Internacionales Regulares')
    charters = models.IntegerField(verbose_name='Pasajeros Charters')
    charters_nacionales = models.IntegerField(verbose_name='Pasajeros Charters Nacionales')
    charters_internacionales = models.IntegerField(verbose_name='Pasajeros Charters Internacionales')

    class Meta:
        app_label = 'ecosistema'
        db_table = "pasajeros_ent_nac"
        ordering = ['-id']


class Report_Section(models.Model):
    title = models.CharField(max_length=100)

class Report(models.Model):
    titulo = models.CharField(max_length=100 ,blank=True)
    nomenclatura = models.CharField(max_length=100 ,blank=True)
    descripcion = RichTextField()
    iframe = models.TextField()
    dimension = models.CharField(max_length=100 ,blank=True)
    ods1  = models.BooleanField(default=False)
    ods2  = models.BooleanField(default=False)
    ods3  = models.BooleanField(default=False)
    ods4  = models.BooleanField(default=False)
    ods5  = models.BooleanField(default=False)
    ods6  = models.BooleanField(default=False)
    ods7  = models.BooleanField(default=False)
    ods8  = models.BooleanField(default=False)
    ods9  = models.BooleanField(default=False)
    ods10 = models.BooleanField(default=False)
    ods11 = models.BooleanField(default=False)
    ods12 = models.BooleanField(default=False)
    ods13 = models.BooleanField(default=False)
    ods14 = models.BooleanField(default=False)
    ods15 = models.BooleanField(default=False)
    ods16 = models.BooleanField(default=False)
    ods17 = models.BooleanField(default=False)
