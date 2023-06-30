from django.forms import ModelForm, TextInput, ClearableFileInput, CheckboxInput, FileInput
from .models import *
from web.models import *
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from django.contrib.auth.models import User, Group
from ckeditor.widgets import CKEditorWidget
from django.core.exceptions import ValidationError
import traceback

# class SeccionChoiceField(forms.ModelChoiceField):
#     def label_from_instance(self, obj):
#         return obj.seccion


# class PublicationForm(forms.ModelForm):
#     section = SeccionChoiceField(queryset=SeccionesCentroDocumental.objects.all(), empty_label=None)
#     category = forms.ModelChoiceField(queryset=Categorias.objects.all(), to_field_name='nombre_categoria', empty_label=None)

#     class Meta:
#         model = Publications
#         fields = ['section', 'category', 'publication', 'visible', 'recent', 'type', 'num_descargas', 'name', 'url']
#         labels = {
#             'section': 'Sección',
#             'category': 'Categoría',
#             'publication': 'Publicación',
#             'visible': 'Visible',
#             'recent': 'Reciente',
#             'type': 'Tipo',
#             'num_descargas': 'Número de descargas',
#             'name': 'Nombre',
#             'url': 'URL',
#         }

class PublicationForm(forms.ModelForm):
    TYPE_CHOICES = (
        ('1', 'PDF'),
        ('2', 'MP3'),
        ('3', 'XLS'),
    )
     
    type = forms.ChoiceField(choices=TYPE_CHOICES, widget=forms.Select(attrs={'class': 'custom-input', 'icon_class': 'fas fa-file'}))
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-user'}))  
    visible = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))
    class Meta:
        model = Publications
        exclude = ('category', 'section', 'num_descargas')
        fields = '__all__'
        widgets = {

            'type': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'name': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-name'}),
            'url': forms.ClearableFileInput(attrs={'class': 'custom-input-file'}),

            'section': TextInput(attrs = { 'placeholder': 'Ingresa una Sección', 'class': 'custom-input'}),
            'category': TextInput(attrs = { 'placeholder': 'Ingresa una Categroia', 'class': 'custom-input'}),            
            'type': TextInput(attrs = { 'placeholder': 'Ingresa un Tipo', 'class': 'custom-input'}),
            'download': TextInput(attrs = { 'placeholder': 'Descarga', 'class': 'custom-input'}),
            'name': TextInput(attrs = { 'placeholder': 'Ingresa un Nombre ', 'class': 'custom-input'}),
            'fiel': ClearableFileInput(attrs = { 'placeholder': 'Ingresa una imagen', 'class': 'custom-input-file'}), 
        }
        labels = {
            'type': 'Tipo de Documento',
            'url': 'Archivo',
            'category': 'Categoria',
        }


class BannerForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = Banner
        fields = '__all__'
        widgets = {
            'name': TextInput(attrs={'placeholder': 'Ingresa una Nombre'}),
            'banner_url': TextInput(attrs={'placeholder': 'Ingresa un Enlace'}),
            'name': TextInput(attrs = { 'placeholder': 'Ingresa una Nombre', 'class': 'custom-input', 'icon_class': 'fas fa-search'}),
            'banner_url': TextInput(attrs = { 'placeholder': 'Ingresa un Enlace','class': 'custom-input', 'icon_class': 'fas fa-globe'}), 
            'activo': CheckboxInput(attrs = { 'class': 'form-check-input'}),
            'imagen': ClearableFileInput(attrs = { 'placeholder': 'Ingresa una imagen', 'class': 'form-control-file'}),
            'subtitulo' : TextInput(attrs = { 'placeholder': 'Ingresa un Subtitulo', 'class': 'custom-input', 'icon_class': 'fas fa-search'}),
            'titulo_pricipal' : TextInput(attrs = { 'placeholder': 'Ingresa una Descripcion', 'class': 'custom-input', 'icon_class': 'fas fa-search'}),
        }


class PlacesOfInterestForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    logotipo = forms.ImageField(widget=forms.ClearableFileInput(attrs={'class': 'form-control-file', 'multiple': True}), label='Logotipo', required=False)
    sitio_web = forms.URLField(widget=forms.TextInput(attrs={'class': 'form-control', 'icon_class': 'fas fa-table', 'placeholder': 'Ingresa un Sitio Web'}), label='Sitio Web')
    description = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'icon_class': 'fas fa-table', 'placeholder': 'Ingresa una Descripción'}), label='Descripción')

    class Meta:
        model = PlacesOfInterest
        fields = ['logotipo', 'sitio_web', 'description']


class PasswordChangeFormCustom(PasswordChangeForm):

    old_password = forms.CharField(
        widget=forms.PasswordInput,
        error_messages={
            'password_incorrect': 'Contraseña actual incorrecta favor de verificar.'}
    )

    def clean_old_password(self):
        old_password = self.cleaned_data.get('old_password')
        if not self.user.check_password(old_password):
            raise forms.ValidationError(
                self.fields['old_password'].error_messages['password_incorrect'],
                code='password_incorrect',
            )
        return old_password

    def clean(self):
        cleaned_data = super().clean()
        new_password1 = cleaned_data.get('new_password1')
        new_password2 = cleaned_data.get('new_password2')

        if new_password1 and new_password2 and new_password1 != new_password2:
            self.add_error('non_field_errors', "Las contraseñas no coinciden")
            return cleaned_data


class DateInput(forms.DateInput):
    input_type = 'date'



class SeccionCentroDocumentalForm(forms.ModelForm):
    class Meta:
        model = SeccionesCentroDocumental
        fields = ['seccion', 'descripcion', 'observacion','imagen']
        widgets = {
            'seccion':forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-search'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control'}),
            'observacion': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-search'}),
        }


class CategoriasForm(forms.ModelForm):

    class Meta:
        model = Categorias
        fields = ['nombre_categoria', 'fecha_creacion', 'seccion']

        widgets = {
            'nombre_categoria': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-search'}),
            'fecha_creacion': forms.DateInput(attrs={'class': 'form-control fecha-input' ,'icon_class': 'fas fa-calendar'}),
        }

    def __init__(self, *args, **kwargs):
        pk = kwargs.pop('pk', None)
        super().__init__(*args, **kwargs)
        if pk:
            seccion = SeccionesCentroDocumental.objects.get(pk=pk)
            self.fields['seccion'].initial = seccion
            self.fields['seccion'].widget = forms.HiddenInput()

# class CategoriasFormUpdate(forms.ModelForm):


class NoticiaForm(ModelForm):

    descripcion = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = Noticia
        fields = '__all__'
        widgets = {

            'titulo': forms.TextInput(attrs={'class': 'custom-input','icon_class': 'fas fa-search'}),
            'sitio_web': forms.TextInput(attrs={'class': 'custom-input','icon_class': 'fas fa-globe'}),
            'fecha_nota': forms.DateInput(attrs={'class': ' custom-input fecha-input','icon_class': 'fas fa-calendar'}),
            'autor_foto': forms.TextInput(attrs={'class': 'custom-input form-control','icon_class': 'fas fa-user'}),
            'autor_nota': forms.TextInput(attrs={'class': ' custom-input form-control','icon_class': 'fas fa-user'}),
            'fecha_recuperacion': forms.DateInput(attrs={'class': ' custom-input fecha-input' ,'icon_class': 'fas fa-calendar'}),
            'imagen': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),

        }


class BarometroForm(forms.ModelForm):
    
    class Meta:
        model = BarometroTuristico
        fields = '__all__'
        exclude = ['num_descargas']
        widgets = {
            'nombrePDF': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-file-pdf'}),
            'yearPDF': forms.NumberInput(attrs={'class': 'custom-input' ,'icon_class': 'fas fa-calendar', 'required': True}),
        }
        labels = {
            'yearPDF': 'Año del PDF',
        }


class AlbaForm(forms.ModelForm):
    class Meta:
        model = Alba
        fields = ['archivo', 'visible']

class DateInput(forms.DateInput):
    input_type = 'date'

class EventoForm(forms.ModelForm):
    
    
    TIPOS_EVENTO_CHOICES = [
        ('', 'Seleccionar'),
        ('internacionales', 'Internacionales'),
        ('nacionales', 'Nacionales'),
        ('estatales', 'Estatales'),
    ]
     
    tipo_evento = forms.ChoiceField(choices=TIPOS_EVENTO_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = Evento
        fields = ['tipo_evento', 'titulo', 'descripcion', 'fecha_inicio', 'fecha_fin', 'imagen']
        widgets = {
            'tipo_evento': forms.TextInput(attrs={'class': 'form-control'}),
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control'}),
            'fecha_inicio': forms.TextInput(attrs={'class': 'form-control fecha-input', 'placeholder': 'Fecha de inicio'}),
            'fecha_fin': forms.TextInput(attrs={'class': 'form-control fecha-input', 'placeholder': 'Fecha de fin'}),
            'imagen': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
        }
        labels = {
            'tipo_evento': 'Tipo de Evento',
        }
    
   
class InventarioHoteleroForm(ModelForm):
    class Meta:
        model = InventarioHotelero
        fields = ['destino', 'fecha', 'categoria', 'habitaciones', 'establecimientos']
        widgets = {
            'destino': forms.TextInput(attrs={'class': 'form-control'}),
            'fecha': forms.DateInput(attrs={'class': 'form-control fecha-input'}),
            'categoria': forms.TextInput(attrs={'class': 'form-control'}),
            'habitaciones': forms.NumberInput(attrs={'class': 'form-control'}),
            'establecimientos': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class CargaMasivaForm(forms.Form):
    archivo = forms.FileField(label='Seleccione un archivo', help_text='(xlsx, csv)')


class GlosarioForm(forms.ModelForm):

    class Meta:
        model = Glosario
        fields = ['palabra', 'definicion']
        labels = {
            'palabra': 'Palabra',
            'definicion': 'Definición',
        }
        widgets = {
            'palabra': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-search'}),
            'definicion': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-book'}),
        }


class DataTurForm(forms.ModelForm):
    class Meta:
        model = DataTour
        fields = '__all__'

class GastoDerramaForm (forms.ModelForm):
    class Meta:
        model = GastoDerrama
        fields = '__all__'


class OtrosAnualesForm (forms.ModelForm):
    class Meta:
        model = otros_anuales
        fields = '__all__'


class ZonasArqueologicasMuseosForm (forms.ModelForm):

    TIPO_CHOICES = (
        ('museo', 'Museo'),
        ('zona arqueologica', 'Zona Arqueológica'),
    )
    tipo = forms.ChoiceField(choices=TIPO_CHOICES, required=False)

    ORIGEN_CHOICES = (
        ('nacional', 'Nacional'),
        ('extranjero', 'Extranjero'),
    )
    origen_visitante = forms.ChoiceField(choices=ORIGEN_CHOICES, required=False)

    class Meta:
        model = zonas_arqueologicas_museos
        fields = ['destino', 'tipo', 'nombre', 'fecha', 'visitantes']

class ZonasArqueologicasMuseosForm_edit (forms.ModelForm):
    TIPO_CHOICES = (
        ('museo', 'Museo'),
        ('zona arqueologica', 'Zona Arqueológica'),
    )
    tipo = forms.ChoiceField(choices=TIPO_CHOICES, required=False)

    class Meta:
        model = zonas_arqueologicas_museos
        fields = '__all__'


class SensivilizacionForm (forms.ModelForm):
    class Meta:
        model = Sensivilizacion
        fields = '__all__'  


class CertificacionForm (forms.ModelForm):
    class Meta:
        model = Certificacion
        fields = '__all__'


class InversionPublicaForm(forms.ModelForm):
    class Meta:
        model = InversionPublica
        fields = ['fecha', 'destino', 'nombre_de_la_obra', 'monto_de_inversion_municipal', 'monto_de_inversion_estatal', 'monto_de_inversion_federal', 'monto_total']
    def __init__ (self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['destino'].widget.attrs['class'] = 'custom-input'
        self.fields['destino'].widget.attrs['icon_class'] = 'fas fa-search'

        self.fields['fecha'].widget.attrs['class'] = 'custom-input'
        self.fields['fecha'].widget.attrs['icon_class'] = 'fas fa-calendar'
        

        self.fields['nombre_de_la_obra'].widget.attrs['class'] = 'custom-input'
        self.fields['nombre_de_la_obra'].widget.attrs['icon_class'] = 'fas fa-search'

        self.fields['monto_de_inversion_municipal'].widget.attrs['class'] = 'custom-input'
        self.fields['monto_de_inversion_municipal'].widget.attrs['icon_class'] = 'fas fa-dollar-sign'

        self.fields['monto_de_inversion_estatal'].widget.attrs['class'] = 'custom-input'
        self.fields['monto_de_inversion_estatal'].widget.attrs['icon_class'] = 'fas fa-dollar-sign'

        self.fields['monto_de_inversion_federal'].widget.attrs['class'] = 'custom-input'
        self.fields['monto_de_inversion_federal'].widget.attrs['icon_class'] = 'fas fa-dollar-sign'

        self.fields['monto_total'].widget.attrs['class'] = 'custom-input'
        self.fields['monto_total'].widget.attrs['icon_class'] = 'fas fa-dollar-sign'



class InventarioHoteleroEntNacForm(ModelForm):

    class Meta:
        model = InventarioHoteleroEntNac
        fields = ['entidad', 'fecha', 'categoria', 'habitaciones', 'establecimientos']
    
    def __init__ (self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['entidad'].widget.attrs['class'] = 'custom-input'
        self.fields['entidad'].widget.attrs['icon_class'] = 'fas fa-search'

        self.fields['fecha'].widget.attrs['class'] = 'custom-input'
        self.fields['fecha'].widget.attrs['icon_class'] = 'fas fa-calendar'

        self.fields['categoria'].widget.attrs['class'] = 'custom-input'
        self.fields['categoria'].widget.attrs['icon_class'] = 'fas fa-search'

        self.fields['habitaciones'].widget.attrs['class'] = 'custom-input'
        self.fields['habitaciones'].widget.attrs['icon_class'] = 'fas fa-table'

        self.fields['establecimientos'].widget.attrs['class'] = 'custom-input'
        self.fields['establecimientos'].widget.attrs['icon_class'] = 'fas fa-table'



class CalidadAireForm(forms.ModelForm):
    class Meta:
        model = CalidadAire
        fields = ['fecha', 'destino', 'calidad_del_aire']
        widgets = {
            'fecha': forms.DateInput(attrs={'class': 'form-control fecha-input'}),
            'destino': forms.TextInput(attrs={'class': 'form-control'}),
            'calidad_del_aire': forms.TextInput(attrs={'class': 'form-control'}),
        },

class ProyectoInversionForm(forms.ModelForm):
    class Meta:
        model = ProyectoInversion
        fields = '__all__'
        widgets = {
            'destino': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Destino'}),
            'nombre_del_proyecto': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre del proyecto'}),
            'promotor_del_proyecto': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Promotor del proyecto'}),
            'referencia_de_ubicacion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Referencia de ubicación'}),
            'zona_turistica': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Zona turística'}),
            'giro': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Giro'}),
            'habitaciones': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Habitaciones'}),
            'empleos_permanentes': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Empleos permanentes'}),
            'empleos_temporales': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Empleos temporales'}),
            'tipo_de_inversion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tipo de inversión'}),
            'origen_de_inversion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Origen de inversión'}),
            'estatus': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Estatus'}),
            'fecha_de_inicio_de_obra': forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'Fecha de inicio de obra'}),
            'fecha_de_conclusion_de_obra': forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'Fecha de conclusión de obra'}),
            'fecha_de_apertura': forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'Fecha de apertura'}),
            'monto_comprometido_del_proyecto_mxn': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Monto comprometido del proyecto (MXN)'}),
            'plazo': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Plazo'}),
            'personas_beneficiadas_con_el_proyecto': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Personas beneficiadas con el proyecto'}),
            'datos_de_contacto': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Datos de contacto'})
        }

# Catalagos
class CatalagoCategoriaForm(forms.ModelForm):
    class Meta:
        model = CatalagoCategoria
        fields = ['categoria']
        labels = {
            'categoria': 'Categoría'
        }
        widgets = {
            'categoria': forms.TextInput(attrs={'class': 'form-control'})
        }

class CatalagoDestinoAeropuertoForm(forms.ModelForm):
    class Meta:
        model = CatalagoDestinoAeropuerto
        fields = ['destino_aeropuerto', 'destino_aeropuerto_id']
        labels = {
            'destino_aeropuerto': 'Destino Aeropuerto',
            'destino_aeropuerto_id': 'ID Destino Aeropuerto'
        }
        widgets = {
            'destino_aeropuerto': forms.TextInput(attrs={'class': 'form-control'}),
            'destino_aeropuerto_id': forms.TextInput(attrs={'class': 'form-control'})
        }

class CatalagoDestinoForm(forms.ModelForm):
    class Meta:
        model = CatalagoDestino
        fields = ['destino', 'entidad']
        labels = {
            'destino': 'Destino',
            'entidad': 'Entidad'
        }
        widgets = {
            'destino': forms.TextInput(attrs={'class': 'form-control'}),
            'entidad': forms.TextInput(attrs={'class': 'form-control'})
        }

class CatalagoSegmentosForm(forms.ModelForm):
    class Meta:
        model = CatalagoSegmentos
        fields = ['segmento']
        labels = {
            'segmento': 'Segmento'
        }
        widgets = {
            'segmento': forms.TextInput(attrs={'class': 'form-control'})
        }

class CatalagoTipoVisistanteForm(forms.ModelForm):
    class Meta:
        model = CatalagoTipoVisistante
        fields = ['tipo_visitante']
        labels = {
            'tipo_visitante': 'Tipo de Visitante'
        }
        widgets = {
            'tipo_visitante': forms.TextInput(attrs={'class': 'form-control'})
        }

class CatalagoZAMuseosForm(forms.ModelForm):
    class Meta:
        model = CatalagoZAMuseos
        fields = ['nombre', 'tipo']
        labels = {
            'nombre': 'Museo/Zona Arqueológica',
            'tipo': 'Tipo'
        }
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'tipo': forms.TextInput(attrs={'class': 'form-control'})
        }

class InversionPrivadaForm (forms.ModelForm):
    class Meta:
        model = inversion_privada
        fields = ['destino','nombre_del_proyecto','fecha','monto_ejecutado','avance_proyecto']

class InversionPrivadaEditForm(forms.ModelForm):
    class Meta:
        model = inversion_privada
        fields = ['id_del_proyecto','nombre_del_proyecto','destino','fecha','monto_ejecutado','avance_proyecto']

class EmpleoForm (forms.ModelForm):
    class Meta:
        model = empleo
        fields ='__all__'

class ModeloGDForm (forms.ModelForm):
    class Meta:
        model = ModeloGD
        fields = '__all__'
        labels = {
            'anio': 'Año',
        }

class CatalogoDestinoForm (forms.ModelForm):
    class Meta:
        model = CatalagoDestino
        fields = '__all__'

class AirbnbForm (forms.ModelForm):
    class Meta:
        model = Airbnb
        fields = '__all__'
class DiscapacidadForm(forms.ModelForm):
    class Meta:
        model = Discapacidad
        fields = '__all__'
        widgets = {
            'destino': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Destino'}),
            'fecha': forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'Fecha'}),
            'giro_comercial': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Giro Comercial'}),
            'empleos_fijos_h': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Empleos Fijos Hombres'}),
            'empleos_fijos_m': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Empleos Fijos Mujeres'}),
            'empleos_temporales_h': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Empleos Temporales Hombres'}),
            'empleos_temporales_m': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Empleos Temporales Mujeres'}),
            'empleados_discapacidad_h': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Empleados Discapacidad Hombres'}),
            'empleados_discapacidad_m': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Empleados Discapacidad Mujeres'}),
        }
        labels = {
            'destino': 'Destino',
            'fecha': 'Fecha',
            'giro_comercial': 'Giro Comercial',
            'empleos_fijos_h': 'Empleos Fijos Hombres',
            'empleos_fijos_m': 'Empleos Fijos Mujeres',
            'empleos_temporales_h': 'Empleos Temporales Hombres',
            'empleos_temporales_m': 'Empleos Temporales Mujeres',
            'empleados_discapacidad_h': 'Empleados Discapacidad Hombres',
            'empleados_discapacidad_m': 'Empleados Discapacidad Mujeres',
        }

class ParticipacionSegmentosForm(forms.ModelForm):
    class Meta:
        model = ParticipacionSegmentos
        fields = ('ano', 'destino', 'segmento', 'participacion')
        labels = {
            'ano': 'Año',
            'destino': 'Destino',
            'segmento': 'Segmento',
            'participacion': 'Participación'
        }
        widgets = {
            'ano': forms.NumberInput(attrs={'class': 'form-control'}),
            'destino': forms.TextInput(attrs={'class': 'form-control'}),
            'segmento': forms.TextInput(attrs={'class': 'form-control'}),
            'participacion': forms.NumberInput(attrs={'class': 'form-control'})
        }

class AeropuertoForm(forms.ModelForm):
    class Meta:
        model = Aeropuerto
        fields = '__all__'
        labels = {
            'pasajeros_aeropuerto_gto': 'Pasajeros en el aeropuerto de Guanajuato',
            'pasajeros_nacionales': 'Pasajeros nacionales',
            'pasajeros_internacionales': 'Pasajeros internacionales',
            'fecha': 'Fecha',
            'vuelos': 'Vuelos'
        }
        widgets = {
            'pasajeros_aeropuerto_gto': forms.NumberInput(attrs={'class': 'form-control'}),
            'pasajeros_nacionales': forms.NumberInput(attrs={'class': 'form-control'}),
            'pasajeros_internacionales': forms.NumberInput(attrs={'class': 'form-control'}),
            'fecha': forms.DateInput(attrs={'class': 'form-control'}),
            'vuelos': forms.TextInput(attrs={'class': 'form-control'}),
        }

class AerolineaForm(forms.ModelForm):
    
    TIPOS_EVENTO_CHOICES = [
        ('Internacional', 'Internacional'),
        ('Nacional', 'Nacional'),
    ]
     
    tipo_aerolinea = forms.ChoiceField(choices=TIPOS_EVENTO_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = Aerolinea
        fields = '__all__'

        widgets = {
            'fecha': forms.TextInput(attrs={'class': 'form-control'}),
            'destino_aeropuerto': forms.TextInput(attrs={'class': 'form-control'}),
            'destino_aeropuerto_id' : forms.TextInput(attrs={'class': 'form-control'}),
            'tipo_aerolinea': forms.TextInput(attrs={'class': 'form-control'}),
            'codigo_aerolinea': forms.TextInput(attrs={'class': 'form-control'}),
        }
    
class ParticipacionOrigenForm (forms.ModelForm):
     class Meta:
        model = ParticipacionOrigen
        fields = '__all__'
        labels = {
            'anio': 'Año',
        }

class FuenteInfoEntornoNForm (forms.ModelForm):
    class Meta:
        model  = FuenteInfoEntornoN
        fields = '__all__'
    
class FuenteInfoPerfilVisitanteEventoForm (forms.ModelForm):
    class Meta:
        model = FuenteInfoPerfilVisitanteEvento
        fields = '__all__'

        labels = {
            'ano': 'Año',
            'codigo_encuesta_ano': 'Código de encuesta año',
        }

class FuenteInfoPerfilVisitanteDestinoForm (forms.ModelForm):

    class Meta:
        model = FuenteInfoPerfilVisitanteDestino
        fields = '__all__'

        labels = {
            'ano': 'Año',
            'codigo_encuesta_ano': 'Código de encuesta año',
        }
        
class InventarioTuristicoForm(forms.ModelForm):
    class Meta:
        model = InventarioTuristico
        fields = '__all__'
        labels = {
            'ano': 'Año',
            'giro': 'Giro',
            'destino': 'Destino',
            'inventario': 'Inventario',
        }
        widgets = {
            'ano': forms.NumberInput(attrs={'class': 'form-control'}),
            'giro': forms.TextInput(attrs={'class': 'form-control'}),
            'destino': forms.TextInput(attrs={'class': 'form-control'}),
            'inventario': forms.NumberInput(attrs={'class': 'form-control'}),
        }


class PasajerosEntNacForm(forms.ModelForm):

    class Meta :
        model = Pasajeros_Ent_Nac
        fields = '__all__'


class DirectorioHoteleroForm(forms.ModelForm):
    class Meta:
        model = DirectorioHotelero
        fields = '__all__'
        labels = {
            'id_establecimiento': 'ID Establecimiento',
            'nombre_de_la_unidad_economica': 'Nombre de la Unidad Económica',
            'razon_social': 'Razón Social',
            'codigo_de_la_clase_de_actividad_scian': 'Código de la Clase de Actividad SCIAN',
            'nombre_de_clase_de_la_actividad': 'Nombre de la Clase de la Actividad',
            'descripcion_estrato_personal_ocupado': 'Descripción del Estrato Personal Ocupado',
            'tipo_de_vialidad': 'Tipo de Vialidad',
            'nombre_de_la_vialidad': 'Nombre de la Vialidad',
            'tipo_de_entre_vialidad_1': 'Tipo de Entre Vialidad 1',
            'nombre_de_entre_vialidad_1': 'Nombre de Entre Vialidad 1',
            'tipo_de_entre_vialidad_2': 'Tipo de Entre Vialidad 2',
            'nombre_de_entre_vialidad_2': 'Nombre de Entre Vialidad 2',
            'tipo_de_entre_vialidad_3': 'Tipo de Entre Vialidad 3',
            'nombre_de_entre_vialidad_3': 'Nombre de Entre Vialidad 3',
            'numero_exterior_o_kilometro': 'Número Exterior o Kilómetro',
            'letra_exterior': 'Letra Exterior',
            'edificio': 'Edificio',
            'edificio_piso': 'Edificio Piso',
            'numero_interior': 'Número Interior',
            'letra_interior': 'Letra Interior',
            'tipo_de_asentamiento_humano': 'Tipo de Asentamiento Humano',
            'nombre_de_asentamiento_humano': 'Nombre de Asentamiento Humano',
            'tipo_centro_comercial': 'Tipo de Centro Comercial',
            'c_industrial_comercial_o_mercado': 'Código Industrial, Comercial o Mercado',
            'numero_de_local': 'Número de Local',
            'codigo_postal': 'Código Postal',
            'clave_entidad': 'Clave de Entidad',
            'entidad_federativa': 'Entidad Federativa',
            'clave_municipio': 'Clave de Municipio',
            'municipio': 'Municipio',
            'clave_localidad': 'Clave de Localidad',
            'localidad': 'Localidad',
            'area_geoestadistica_basica': 'Área Geoestadística Básica',
            'manzana': 'Manzana',
            'numero_de_telefono': 'Número de Teléfono',
            'correo_electronico': 'Correo Electrónico',
            'sitio_en_internet': 'Sitio en Internet',
            'tipo_de_establecimiento': 'Tipo de Establecimiento',
            'latitud': 'Latitud',
            'longitud': 'Longitud',
            'fecha_de_incorporacion_al_denue': 'Fecha de Incorporación al DENUE',
            'categoria_turistica': 'Categoría Turística',
            'no_cuartos': 'Número de Cuartos',
            'unidades': 'Unidades',
            'espacios_cajones': 'Espacios de Cajones',
            'no_camas': 'Número de Camas',
            'cadena': 'Cadena',
            'operadora': 'Operadora',
            'responsable': 'Responsable',
            'cargo': 'Cargo',
            'imss': 'IMSS',
            'inicio_de_operaciones_este_ano': 'Inicio de Operaciones este Año',
            'fecha_de_inicio_de_operaciones': 'Fecha de Inicio de Operaciones',
            'centro_turistico': 'Centro Turístico',
            'zona': 'Zona',
            'datatur': 'Datatur',
            'hotel_boutique': 'Hotel Boutique',
            'nombre_de_la_cadena': 'Nombre de la Cadena',
            'hoteles_tesoros': 'Hoteles Tesoros',
        }
        widgets = {
            'id_establecimiento': forms.NumberInput(attrs={'class': 'form-control'}),
            'nombre_de_la_unidad_economica': forms.TextInput(attrs={'class': 'form-control'}),
            'razon_social': forms.TextInput(attrs={'class': 'form-control'}),
            'codigo_de_la_clase_de_actividad_scian': forms.NumberInput(attrs={'class': 'form-control'}),
            'nombre_de_clase_de_la_actividad': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion_estrato_personal_ocupado': forms.TextInput(attrs={'class': 'form-control'}),
            'tipo_de_vialidad': forms.TextInput(attrs={'class': 'form-control'}),
            'nombre_de_la_vialidad': forms.TextInput(attrs={'class': 'form-control'}),
            'tipo_de_entre_vialidad_1': forms.TextInput(attrs={'class': 'form-control'}),
            'nombre_de_entre_vialidad_1': forms.TextInput(attrs={'class': 'form-control'}),
            'tipo_de_entre_vialidad_2': forms.TextInput(attrs={'class': 'form-control'}),
            'nombre_de_entre_vialidad_2': forms.TextInput(attrs={'class': 'form-control'}),
            'tipo_de_entre_vialidad_3': forms.TextInput(attrs={'class': 'form-control'}),
            'nombre_de_entre_vialidad_3': forms.TextInput(attrs={'class': 'form-control'}),
            'numero_exterior_o_kilometro': forms.TextInput(attrs={'class': 'form-control'}),
            'letra_exterior': forms.TextInput(attrs={'class': 'form-control'}),
            'edificio': forms.TextInput(attrs={'class': 'form-control'}),
            'edificio_piso': forms.NumberInput(attrs={'class': 'form-control'}),
            'numero_interior': forms.NumberInput(attrs={'class': 'form-control'}),
            'letra_interior': forms.TextInput(attrs={'class': 'form-control'}),
            'tipo_de_asentamiento_humano': forms.TextInput(attrs={'class': 'form-control'}),
            'nombre_de_asentamiento_humano': forms.TextInput(attrs={'class': 'form-control'}),
            'tipo_centro_comercial': forms.TextInput(attrs={'class': 'form-control'}),
            'c_industrial_comercial_o_mercado': forms.TextInput(attrs={'class': 'form-control'}),
            'numero_de_local': forms.NumberInput(attrs={'class': 'form-control'}),
            'codigo_postal': forms.TextInput(attrs={'class': 'form-control'}),
            'clave_entidad': forms.NumberInput(attrs={'class': 'form-control'}),
            'entidad_federativa': forms.TextInput(attrs={'class': 'form-control'}),
            'clave_municipio': forms.NumberInput(attrs={'class': 'form-control'}),
            'municipio': forms.TextInput(attrs={'class': 'form-control'}),
            'clave_localidad': forms.NumberInput(attrs={'class': 'form-control'}),
            'localidad': forms.TextInput(attrs={'class': 'form-control'}),
            'area_geoestadistica_basica': forms.TextInput(attrs={'class': 'form-control'}),
            'manzana': forms.NumberInput(attrs={'class': 'form-control'}),
            'numero_de_telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'correo_electronico': forms.TextInput(attrs={'class': 'form-control'}),
            'sitio_en_internet': forms.TextInput(attrs={'class': 'form-control'}),
            'tipo_de_establecimiento': forms.TextInput(attrs={'class': 'form-control'}),
            'latitud': forms.NumberInput(attrs={'class': 'form-control'}),
            'longitud': forms.NumberInput(attrs={'class': 'form-control'}),
            'fecha_de_incorporacion_al_denue': forms.DateInput(attrs={'class': 'form-control'}),
            'categoria_turistica': forms.TextInput(attrs={'class': 'form-control'}),
            'no_cuartos': forms.NumberInput(attrs={'class': 'form-control'}),
            'unidades': forms.NumberInput(attrs={'class': 'form-control'}),
            'espacios_cajones': forms.NumberInput(attrs={'class': 'form-control'}),
            'no_camas': forms.NumberInput(attrs={'class': 'form-control'}),
            'cadena': forms.NumberInput(attrs={'class': 'form-control'}),
            'operadora': forms.NumberInput(attrs={'class': 'form-control'}),
            'responsable': forms.TextInput(attrs={'class': 'form-control'}),
            'cargo': forms.TextInput(attrs={'class': 'form-control'}),
            'imss': forms.NumberInput(attrs={'class': 'form-control'}),
            'inicio_de_operaciones_este_ano': forms.TextInput(attrs={'class': 'form-control'}),
            'fecha_de_inicio_de_operaciones': forms.DateInput(attrs={'class': 'form-control'}),
            'centro_turistico': forms.TextInput(attrs={'class': 'form-control'}),
            'zona': forms.TextInput(attrs={'class': 'form-control'}),
            'datatur': forms.TextInput(attrs={'class': 'form-control'}),
            'hotel_boutique': forms.NumberInput(attrs={'class': 'form-control'}),
            'nombre_de_la_cadena': forms.TextInput(attrs={'class': 'form-control'}),
            'hoteles_tesoros': forms.TextInput(attrs={'class': 'form-control'}),
        }

#Direcctorio Turistico
class DirectorioAgenciasDeViajesForm(forms.ModelForm):
    class Meta:
        model = DirectorioAgenciasDeViajes
        fields = '__all__'
        labels = {
            'giro': 'Giro',
            'clave_del_giro': 'Clave del Giro',
            'entidad': 'Entidad',
            'clave_entidad': 'Clave de Entidad',
            'destino': 'Destino',
            'clave_municipio': 'Clave de Municipio',
            'nombre_comercial': 'Nombre Comercial',
            'razon_social': 'Razón Social',
            'rfc': 'RFC',
            'calle': 'Calle',
            'numero': 'Número',
            'colonia': 'Colonia',
            'codigo_postal': 'Código Postal',
            'lada': 'Lada',
            'telefono_1': 'Teléfono 1',
            'telefono_2': 'Teléfono 2',
            'celular': 'Celular',
            'correo_electronico': 'Correo Electrónico',
            'sitio_web': 'Sitio Web',
            'ret': 'RET',
            'rnt': 'RNT'
        }
        widgets = {
            'giro': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'clave_del_giro': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'entidad': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-search'}),
            'clave_entidad': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'destino': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-search'}),
            'clave_municipio': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'nombre_comercial': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'razon_social': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'rfc': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'calle': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'numero': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'colonia': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'codigo_postal': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'lada': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'telefono_1': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'telefono_2': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'celular': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'correo_electronico': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-envelope'}),
            'sitio_web': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-globe'}),
            'ret': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'rnt': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
        }

class DirectorioAlimentosYBebidasForm(forms.ModelForm):
    class Meta:
        model = DirectorioAlimentosYBebidas
        fields = '__all__'
        labels = {
            'giro': 'Giro',
            'clave_del_giro': 'Clave del Giro',
            'entidad': 'Entidad',
            'clave_entidad': 'Clave de Entidad',
            'destino': 'Destino',
            'clave_municipio': 'Clave de Municipio',
            'nombre_comercial': 'Nombre Comercial',
            'razon_social': 'Razón Social',
            'rfc': 'RFC',
            'calle': 'Calle',
            'numero': 'Número',
            'colonia': 'Colonia',
            'codigo_postal': 'Código Postal',
            'lada': 'Lada',
            'telefono_1': 'Teléfono 1',
            'telefono_2': 'Teléfono 2',
            'celular': 'Celular',
            'correo_electronico': 'Correo Electrónico',
            'sitio_web': 'Sitio Web',
            'ret': 'RET',
            'rnt': 'RNT'
        }
        widgets = {
            'giro': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'clave_del_giro': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'entidad': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-search'}),
            'clave_entidad': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'destino': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-search'}),
            'clave_municipio': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'nombre_comercial': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'razon_social': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'rfc': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'calle': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'numero': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'colonia': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'codigo_postal': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'lada': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'telefono_1': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'telefono_2': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'celular': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'correo_electronico': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-envelope'}),
            'sitio_web': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-globe'}),
            'ret': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'rnt': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
        }

class DirectorioArrendadorasForm(forms.ModelForm):
    class Meta:
        model = DirectorioArrendadoras
        fields = '__all__'
        widgets = {
            'giro': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'clave_del_giro': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'entidad': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'clave_entidad': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'destino': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'clave_municipio': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'nombre_comercial': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'razon_social': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'rfc': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'calle': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'numero': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'colonia': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'codigo_postal': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'lada': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'telefono_1': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'telefono_2': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'celular': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'correo_electronico': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-envelope'}),
            'sitio_web': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-globe'}),
            'ret': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'rnt': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
        }

class DirectorioActivosRecreacionYDeporteForm(forms.ModelForm):
    class Meta:
        model = DirectorioActivosRecreacionYDeporte
        fields = '__all__'
        labels = {
            'giro': 'Giro',
            'clave_del_giro': 'Clave del Giro',
            'entidad': 'Entidad',
            'clave_entidad': 'Clave de Entidad',
            'destino': 'Destino',
            'clave_municipio': 'Clave de Municipio',
            'nombre_comercial': 'Nombre Comercial',
            'razon_social': 'Razón Social',
            'rfc': 'RFC',
            'calle': 'Calle',
            'numero': 'Número',
            'colonia': 'Colonia',
            'codigo_postal': 'Código Postal',
            'lada': 'Lada',
            'telefono_1': 'Teléfono 1',
            'telefono_2': 'Teléfono 2',
            'celular': 'Celular',
            'correo_electronico': 'Correo Electrónico',
            'sitio_web': 'Sitio Web',
            'ret': 'RET',
            'rnt': 'RNT'
        }
        widgets = {
            'giro': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'clave_del_giro': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'entidad': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'clave_entidad': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'destino': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'clave_municipio': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'nombre_comercial': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'razon_social': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'rfc': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'calle': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'numero': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'colonia': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'codigo_postal': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'lada': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'telefono_1': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'telefono_2': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'celular': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'correo_electronico': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'sitio_web': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'ret': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'rnt': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
        }

class DirectorioAuxilioTuristicoForm(forms.ModelForm):
    class Meta:
        model = DirectorioAuxilioTuristico
        fields = '__all__'
        labels = {
            'giro': 'Giro',
            'clave_del_giro': 'Clave del Giro',
            'entidad': 'Entidad',
            'clave_entidad': 'Clave de Entidad',
            'destino': 'Destino',
            'clave_municipio': 'Clave de Municipio',
            'nombre_comercial': 'Nombre Comercial',
            'razon_social': 'Razón Social',
            'rfc': 'RFC',
            'calle': 'Calle',
            'numero': 'Número',
            'colonia': 'Colonia',
            'codigo_postal': 'Código Postal',
            'lada': 'Lada',
            'telefono_1': 'Teléfono 1',
            'telefono_2': 'Teléfono 2',
            'celular': 'Celular',
            'correo_electronico': 'Correo Electrónico',
            'sitio_web': 'Sitio Web',
            'ret': 'RET',
            'rnt': 'RNT'
        }
        widgets = {
            'giro': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'clave_del_giro': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'entidad': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'clave_entidad': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'destino': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'clave_municipio': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'nombre_comercial': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'razon_social': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'rfc': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'calle': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'numero': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'colonia': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'codigo_postal': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'lada': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'telefono_1': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'telefono_2': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'celular': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'correo_electronico': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'sitio_web': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'ret': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'rnt': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
        }

class DirectorioBalneariosParquesAcuaticosForm(forms.ModelForm):
    class Meta:
        model = DirectorioBalneariosParquesAcuaticos
        fields = '__all__'
        widgets = {
            'giro': forms.TextInput(attrs={'class': 'form-control', 'icon_class': 'fas fa-table'}),
            'clave_del_giro': forms.NumberInput(attrs={'class': 'form-control', 'icon_class': 'fas fa-table'}),
            'entidad': forms.TextInput(attrs={'class': 'form-control', 'icon_class': 'fas fa-table'}),
            'clave_entidad': forms.NumberInput(attrs={'class': 'form-control', 'icon_class': 'fas fa-table'}),
            'destino': forms.TextInput(attrs={'class': 'form-control', 'icon_class': 'fas fa-table'}),
            'clave_municipio': forms.NumberInput(attrs={'class': 'form-control', 'icon_class': 'fas fa-table'}),
            'nombre_comercial': forms.TextInput(attrs={'class': 'form-control', 'icon_class': 'fas fa-table'}),
            'razon_social': forms.TextInput(attrs={'class': 'form-control', 'icon_class': 'fas fa-table'}),
            'rfc': forms.TextInput(attrs={'class': 'form-control', 'icon_class': 'fas fa-table'}),
            'calle': forms.TextInput(attrs={'class': 'form-control', 'icon_class': 'fas fa-table'}),
            'numero': forms.TextInput(attrs={'class': 'form-control', 'icon_class': 'fas fa-table'}),
            'colonia': forms.TextInput(attrs={'class': 'form-control', 'icon_class': 'fas fa-table'}),
            'codigo_postal': forms.TextInput(attrs={'class': 'form-control', 'icon_class': 'fas fa-table'}),
            'lada': forms.TextInput(attrs={'class': 'form-control', 'icon_class': 'fas fa-table'}),
            'telefono_1': forms.TextInput(attrs={'class': 'form-control', 'icon_class': 'fas fa-table'}),
            'telefono_2': forms.TextInput(attrs={'class': 'form-control', 'icon_class': 'fas fa-table'}),
            'celular': forms.TextInput(attrs={'class': 'form-control', 'icon_class': 'fas fa-table'}),
            'correo_electronico': forms.TextInput(attrs={'class': 'form-control', 'icon_class': 'fas fa-envelope'}),
            'sitio_web': forms.TextInput(attrs={'class': 'form-control', 'icon_class': 'fas fa-globe'}),
            'ret': forms.TextInput(attrs={'class': 'form-control', 'icon_class': 'fas fa-table'}),
            'rnt': forms.TextInput(attrs={'class': 'form-control', 'icon_class': 'fas fa-table'}),
            'numero_albercas': forms.TextInput(attrs={'class': 'form-control', 'icon_class': 'fas fa-table'}),
            'numero_toboganes': forms.TextInput(attrs={'class': 'form-control', 'icon_class': 'fas fa-table'}),
            'aguas_termales': forms.TextInput(attrs={'class': 'form-control', 'icon_class': 'fas fa-table'}),
        }

class DirectorioCampoDeGolfForm(forms.ModelForm):
    class Meta:
        model = DirectorioCampoDeGolf
        fields = '__all__'

        widgets = {
            'giro': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'clave_del_giro': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'entidad': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'clave_entidad': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'destino': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'clave_municipio': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'nombre_comercial': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'razon_social': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'rfc': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'calle': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'numero': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'colonia': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'codigo_postal': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'lada': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'telefono_1': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'telefono_2': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'celular': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'correo_electronico': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'sitio_web': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'ret': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'rnt': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
        }

class DirectorioCapacitacionTuristicaForm(forms.ModelForm):
    class Meta:
        model = DirectorioCapacitacionTuristica
        fields = '__all__'
        labels = {
            'giro': 'Giro',
            'clave_del_giro': 'Clave del Giro',
            'entidad': 'Entidad',
            'clave_entidad': 'Clave de Entidad',
            'destino': 'Destino',
            'clave_municipio': 'Clave de Municipio',
            'nombre_comercial': 'Nombre Comercial',
            'razon_social': 'Razón Social',
            'rfc': 'RFC',
            'calle': 'Calle',
            'numero': 'Número',
            'colonia': 'Colonia',
            'codigo_postal': 'Código Postal',
            'lada': 'Lada',
            'telefono_1': 'Teléfono 1',
            'telefono_2': 'Teléfono 2',
            'celular': 'Celular',
            'correo_electronico': 'Correo Electrónico',
            'sitio_web': 'Sitio Web',
            'ret': 'RET',
            'tipo': 'Tipo',
            'lic_gastronomia': 'Licencia de Gastronomía',
            'lic_turismo': 'Licencia de Turismo',
            'posgrado_en_turismo': 'Posgrado en Turismo',
            'certificacion_como_guia_de_turista': 'Certificación como Guía de Turista',
            'otros_estudios_en_turismo': 'Otros Estudios en Turismo',
            'rnt': 'RNT',
        }
        widgets = {
            'giro': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'clave_del_giro': forms.NumberInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'entidad': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'clave_entidad': forms.NumberInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'destino': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'clave_municipio': forms.NumberInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'nombre_comercial': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'razon_social': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'rfc': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'calle': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'numero': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'colonia': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'codigo_postal': forms.NumberInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'lada': forms.NumberInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'telefono_1': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'telefono_2': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'celular': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'correo_electronico': forms.EmailInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'sitio_web': forms.URLInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'ret': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'tipo': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'lic_gastronomia': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'lic_turismo': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'posgrado_en_turismo': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'certificacion_como_guia_de_turista': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'otros_estudios_en_turismo': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'rnt': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
        }

class DirectorioGuiasDeTuristasForm(forms.ModelForm):
    class Meta:
        model = DirectorioGuiasDeTuristas
        fields = '__all__'
        labels = {
            'giro': 'Giro',
            'clave_del_giro': 'Clave del Giro',
            'entidad': 'Entidad',
            'clave_entidad': 'Clave de Entidad',
            'destino': 'Destino',
            'clave_municipio': 'Clave de Municipio',
            'nombre_comercial': 'Nombre Comercial',
            'razon_social': 'Razón Social',
            'rfc': 'RFC',
            'calle': 'Calle',
            'numero': 'Número',
            'colonia': 'Colonia',
            'codigo_postal': 'Código Postal',
            'lada': 'Lada',
            'telefono_1': 'Teléfono 1',
            'telefono_2': 'Teléfono 2',
            'celular': 'Celular',
            'correo_electronico': 'Correo Electrónico',
            'sitio_web': 'Sitio Web',
            'ret': 'RET',
            'rnt': 'RNT',
            'tipo': 'Tipo',
            'no_acreditacion': 'No. de Acreditación',
            'vigencia_acreditacion': 'Vigencia de Acreditación',
            'especialidad': 'Especialidad',
        }
    def __init__ (self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['giro'].widget.attrs['class'] = 'custom-input'
        self.fields['giro'].widget.attrs['icon_class'] = 'fas fa-table'
        self.fields['clave_del_giro'].widget.attrs['class'] = 'custom-input'
        self.fields['clave_del_giro'].widget.attrs['icon_class'] = 'fas fa-table'
        self.fields['entidad'].widget.attrs['class'] = 'custom-input'
        self.fields['entidad'].widget.attrs['icon_class'] = 'fas fa-table'
        self.fields['clave_entidad'].widget.attrs['class'] = 'custom-input'
        self.fields['clave_entidad'].widget.attrs['icon_class'] = 'fas fa-table'
        self.fields['destino'].widget.attrs['class'] = 'custom-input'
        self.fields['destino'].widget.attrs['icon_class'] = 'fas fa-table'
        self.fields['clave_municipio'].widget.attrs['class'] = 'custom-input'
        self.fields['clave_municipio'].widget.attrs['icon_class'] = 'fas fa-table'
        self.fields['nombre_comercial'].widget.attrs['class'] = 'custom-input'
        self.fields['nombre_comercial'].widget.attrs['icon_class'] = 'fas fa-table'
        self.fields['razon_social'].widget.attrs['class'] = 'custom-input'
        self.fields['razon_social'].widget.attrs['icon_class'] = 'fas fa-table'
        self.fields['rfc'].widget.attrs['class'] = 'custom-input'
        self.fields['rfc'].widget.attrs['icon_class'] = 'fas fa-table'
        self.fields['calle'].widget.attrs['class'] = 'custom-input'
        self.fields['calle'].widget.attrs['icon_class'] = 'fas fa-table'
        self.fields['numero'].widget.attrs['class'] = 'custom-input'
        self.fields['numero'].widget.attrs['icon_class'] = 'fas fa-table'
        self.fields['colonia'].widget.attrs['class'] = 'custom-input'
        self.fields['colonia'].widget.attrs['icon_class'] = 'fas fa-table'
        self.fields['codigo_postal'].widget.attrs['class'] = 'custom-input'
        self.fields['codigo_postal'].widget.attrs['icon_class'] = 'fas fa-table'
        self.fields['lada'].widget.attrs['class'] = 'custom-input'
        self.fields['lada'].widget.attrs['icon_class'] = 'fas fa-table'
        self.fields['telefono_1'].widget.attrs['class'] = 'custom-input'
        self.fields['telefono_1'].widget.attrs['icon_class'] = 'fas fa-table'
        self.fields['telefono_2'].widget.attrs['class'] = 'custom-input'
        self.fields['telefono_2'].widget.attrs['icon_class'] = 'fas fa-table'
        self.fields['celular'].widget.attrs['class'] = 'custom-input'
        self.fields['celular'].widget.attrs['icon_class'] = 'fas fa-table'
        self.fields['correo_electronico'].widget.attrs['class'] = 'custom-input'
        self.fields['correo_electronico'].widget.attrs['icon_class'] = 'fas fa-envelope'
        self.fields['sitio_web'].widget.attrs['class'] = 'custom-input'
        self.fields['sitio_web'].widget.attrs['icon_class'] = 'fas fa-globe'
        self.fields['ret'].widget.attrs['class'] = 'custom-input'
        self.fields['ret'].widget.attrs['icon_class'] = 'fas fa-table'
        self.fields['rnt'].widget.attrs['class'] = 'custom-input'
        self.fields['rnt'].widget.attrs['icon_class'] = 'fas fa-table'
        self.fields['tipo'].widget.attrs['class'] = 'custom-input'
        self.fields['tipo'].widget.attrs['icon_class'] = 'fas fa-table'
        self.fields['no_acreditacion'].widget.attrs['class'] = 'custom-input'
        self.fields['no_acreditacion'].widget.attrs['icon_class'] = 'fas fa-table'
        self.fields['vigencia_acreditacion'].widget.attrs['class'] = 'custom-input'
        self.fields['vigencia_acreditacion'].widget.attrs['icon_class'] = 'fas fa-table'
        self.fields['especialidad'].widget.attrs['class'] = 'custom-input'
        self.fields['especialidad'].widget.attrs['icon_class'] = 'fas fa-table'
        



class DirectorioOperadoresForm(forms.ModelForm):
    class Meta:
        model = DirectorioOperadores
        fields = '__all__'
        labels = {
            'giro': 'Giro',
            'clave_del_giro': 'Clave del Giro',
            'entidad': 'Entidad',
            'clave_entidad': 'Clave de Entidad',
            'destino': 'Destino',
            'clave_municipio': 'Clave de Municipio',
            'nombre_comercial': 'Nombre Comercial',
            'razon_social': 'Razón Social',
            'rfc': 'RFC',
            'calle': 'Calle',
            'numero': 'Número',
            'colonia': 'Colonia',
            'codigo_postal': 'Código Postal',
            'lada': 'Lada',
            'telefono_1': 'Teléfono 1',
            'telefono_2': 'Teléfono 2',
            'celular': 'Celular',
            'correo_electronico': 'Correo Electrónico',
            'sitio_web': 'Sitio Web',
            'ret': 'RET',
            'rnt': 'RNT'
        }
        widgets = {
            'giro': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'clave_del_giro': forms.NumberInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'entidad': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'clave_entidad': forms.NumberInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'destino': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'clave_municipio': forms.NumberInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'nombre_comercial': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'razon_social': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'rfc': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'calle': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'numero': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'colonia': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'codigo_postal': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'lada': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'telefono_1': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'telefono_2': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'celular': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'correo_electronico': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'sitio_web': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'ret': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'rnt': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'})
        }

class DirectorioProductosTuristicosForm(forms.ModelForm):
    class Meta:
        model = DirectorioProductosTuristicos
        fields = '__all__'
        labels = {
            'giro': 'Giro',
            'clave_del_giro': 'Clave del Giro',
            'entidad': 'Entidad',
            'clave_entidad': 'Clave de Entidad',
            'destino': 'Destino',
            'clave_municipio': 'Clave de Municipio',
            'nombre_comercial': 'Nombre Comercial',
            'razon_social': 'Razón Social',
            'rfc': 'RFC',
            'calle': 'Calle',
            'numero': 'Número',
            'colonia': 'Colonia',
            'codigo_postal': 'Código Postal',
            'lada': 'Lada',
            'telefono_1': 'Teléfono 1',
            'telefono_2': 'Teléfono 2',
            'celular': 'Celular',
            'correo_electronico': 'Correo Electrónico',
            'sitio_web': 'Sitio Web',
            'ret': 'RET',
            'rnt': 'RNT',
            'segmento': 'Segmento'
        }
    def __init__ (self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['giro'].widget.attrs['class'] = 'custom-input'
        self.fields['giro'].widget.attrs['icon_class'] = 'fas fa-table'
        self.fields['clave_del_giro'].widget.attrs['class'] = 'custom-input'
        self.fields['clave_del_giro'].widget.attrs['icon_class'] = 'fas fa-table'
        self.fields['entidad'].widget.attrs['class'] = 'custom-input'
        self.fields['entidad'].widget.attrs['icon_class'] = 'fas fa-table'
        self.fields['clave_entidad'].widget.attrs['class'] = 'custom-input'
        self.fields['clave_entidad'].widget.attrs['icon_class'] = 'fas fa-table'
        self.fields['destino'].widget.attrs['class'] = 'custom-input'
        self.fields['destino'].widget.attrs['icon_class'] = 'fas fa-table'
        self.fields['clave_municipio'].widget.attrs['class'] = 'custom-input'
        self.fields['clave_municipio'].widget.attrs['icon_class'] = 'fas fa-table'
        self.fields['nombre_comercial'].widget.attrs['class'] = 'custom-input'
        self.fields['nombre_comercial'].widget.attrs['icon_class'] = 'fas fa-table'
        self.fields['razon_social'].widget.attrs['class'] = 'custom-input'
        self.fields['razon_social'].widget.attrs['icon_class'] = 'fas fa-table'
        self.fields['rfc'].widget.attrs['class'] = 'custom-input'
        self.fields['rfc'].widget.attrs['icon_class'] = 'fas fa-table'
        self.fields['calle'].widget.attrs['class'] = 'custom-input'
        self.fields['calle'].widget.attrs['icon_class'] = 'fas fa-table'
        self.fields['numero'].widget.attrs['class'] = 'custom-input'
        self.fields['numero'].widget.attrs['icon_class'] = 'fas fa-table'
        self.fields['colonia'].widget.attrs['class'] = 'custom-input'
        self.fields['colonia'].widget.attrs['icon_class'] = 'fas fa-table'
        self.fields['codigo_postal'].widget.attrs['class'] = 'custom-input'
        self.fields['codigo_postal'].widget.attrs['icon_class'] = 'fas fa-table'
        self.fields['lada'].widget.attrs['class'] = 'custom-input'
        self.fields['lada'].widget.attrs['icon_class'] = 'fas fa-table'
        self.fields['telefono_1'].widget.attrs['class'] = 'custom-input'
        self.fields['telefono_1'].widget.attrs['icon_class'] = 'fas fa-table'
        self.fields['telefono_2'].widget.attrs['class'] = 'custom-input'
        self.fields['telefono_2'].widget.attrs['icon_class'] = 'fas fa-table'
        self.fields['celular'].widget.attrs['class'] = 'custom-input'
        self.fields['celular'].widget.attrs['icon_class'] = 'fas fa-table'
        self.fields['correo_electronico'].widget.attrs['class'] = 'custom-input'
        self.fields['correo_electronico'].widget.attrs['icon_class'] = 'fas fa-envelope'
        self.fields['sitio_web'].widget.attrs['class'] = 'custom-input'
        self.fields['sitio_web'].widget.attrs['icon_class'] = 'fas fa-globe'
        self.fields['ret'].widget.attrs['class'] = 'custom-input'
        self.fields['ret'].widget.attrs['icon_class'] = 'fas fa-table'
        self.fields['rnt'].widget.attrs['class'] = 'custom-input'
        self.fields['rnt'].widget.attrs['icon_class'] = 'fas fa-table'
        self.fields['segmento'].widget.attrs['class'] = 'custom-input'
        self.fields['segmento'].widget.attrs['icon_class'] = 'fas fa-table'









class DirectorioRecintosAuditoriosYSalonesForm(forms.ModelForm):
    class Meta:
        model = DirectorioRecintosAuditoriosYSalones
        fields = '__all__'
        labels = {
            'giro': 'Giro',
            'clave_del_giro': 'Clave del Giro',
            'entidad': 'Entidad',
            'clave_entidad': 'Clave de Entidad',
            'destino': 'Destino',
            'clave_municipio': 'Clave de Municipio',
            'nombre_comercial': 'Nombre Comercial',
            'razon_social': 'Razón Social',
            'rfc': 'RFC',
            'calle': 'Calle',
            'numero': 'Número',
            'colonia': 'Colonia',
            'codigo_postal': 'Código Postal',
            'lada': 'Lada',
            'telefono_1': 'Teléfono 1',
            'telefono_2': 'Teléfono 2',
            'celular': 'Celular',
            'correo_electronico': 'Correo Electrónico',
            'sitio_web': 'Sitio Web',
            'ret': 'RET',
            'rnt': 'RNT',
            'modalidad': 'Modalidad',
            'depende_de_hotel_o_restaurante':'Depende de hotel o restaurante',
            'no_de_salones':'no de salones',
            'capacidad_maxima':'Capacidad maxima',
        }
        widgets = {
            'giro': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'clave_del_giro': forms.NumberInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'entidad': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'clave_entidad': forms.NumberInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'destino': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'clave_municipio': forms.NumberInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'nombre_comercial': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'razon_social': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'rfc': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'calle': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'numero': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'colonia': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'codigo_postal': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'lada': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'telefono_1': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'telefono_2': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'celular': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'correo_electronico': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-envelope'}),
            'sitio_web': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-globe'}),
            'ret': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'rnt': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'modalidad': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'depende_de_hotel_o_restaurante': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'no_de_salones': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'capacidad_maxima': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
        }

class DirectorioSpaForm(forms.ModelForm):
    class Meta:
        model = DirectorioSpa
        fields = '__all__'
        labels = {
            'giro': 'Giro',
            'clave_del_giro': 'Clave del Giro',
            'entidad': 'Entidad',
            'clave_entidad': 'Clave de Entidad',
            'destino': 'Destino',
            'clave_municipio': 'Clave de Municipio',
            'nombre_comercial': 'Nombre Comercial',
            'razon_social': 'Razón Social',
            'rfc': 'RFC',
            'calle': 'Calle',
            'numero': 'Número',
            'colonia': 'Colonia',
            'codigo_postal': 'Código Postal',
            'lada': 'Lada',
            'telefono_1': 'Teléfono 1',
            'telefono_2': 'Teléfono 2',
            'celular': 'Celular',
            'correo_electronico': 'Correo Electrónico',
            'sitio_web': 'Sitio Web',
            'ret': 'RET',
            'rnt': 'RNT'
        }
        widgets = {
            'giro': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'clave_del_giro': forms.NumberInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'entidad': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'clave_entidad': forms.NumberInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'destino': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'clave_municipio': forms.NumberInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'nombre_comercial': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'razon_social': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'rfc': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'calle': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'numero': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'colonia': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'codigo_postal': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'lada': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'telefono_1': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'telefono_2': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'celular': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'correo_electronico': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'sitio_web': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'ret': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'rnt': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'})
        }


class EncuestaFormB(forms.ModelForm):

    TYPE_CHOICES = (
        (1, 'Barometro'),
        (2, 'ENIOT'),
    )

    seccion = forms.ChoiceField(choices=TYPE_CHOICES, widget=forms.Select(attrs={'class': 'custom-input', 'icon_class': 'fas fa-file'}))
    url = forms.URLField(widget=forms.URLInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-globe'}))
    activo = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))

    class Meta:
        model = Encuesta
        fields = '__all__'


class   ReporteMensualForm(forms.ModelForm):
    MES_CHOICES = (
        (1, 'Enero'),
        (2, 'Febrero'),
        (3, 'Marzo'),
        (4, 'Abril'),
        (5, 'Mayo'),
        (6, 'Junio'),
        (7, 'Julio'),
        (8, 'Agosto'),
        (9, 'Septiembre'),
        (10, 'Octubre'),
        (11, 'Noviembre'),
        (12, 'Diciembre'),
    )

    mes = forms.ChoiceField(choices=MES_CHOICES, widget=forms.Select(attrs={'class': 'custom-input', 'icon_class': 'fas fa-calendar'}))

    class Meta:
        model = Reportes_Mensuales
        fields = '__all__'
        exclude = ['num_descargas']

        labels = {'ano': 'Año', }
        
    def __init__ (self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['ano'].widget.attrs['class'] = 'custom-input'
        self.fields['ano'].widget.attrs['icon_class'] = 'fas fa-calendar'

        self.fields['titulo'].widget.attrs['class'] = 'custom-input'
        self.fields['titulo'].widget.attrs['icon_class'] = 'fas fa-search'

 




class ReportsForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = '__all__'

    def __init__ (self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['titulo'].widget.attrs['class'] = 'custom-input'
        self.fields['titulo'].widget.attrs['icon_class'] = 'fas fa-search'

        self.fields['nomenclatura'].widget.attrs['class'] = 'custom-input'
        self.fields['nomenclatura'].widget.attrs['icon_class'] = 'fas fa-search'
        self.fields['dimension'].widget.attrs['class'] = 'custom-input'
        self.fields['dimension'].widget.attrs['icon_class'] = 'fas fa-search'

        self.fields['iframe'].widget.attrs['class'] = 'custom-input'
        self.fields['iframe'].widget.attrs['icon_class'] = 'fas fa-search'

        self.fields['ods1'].widget.attrs['class'] = ''
        self.fields['ods2'].widget.attrs['class'] = 'form-check-input'
        self.fields['ods3'].widget.attrs['class'] = 'form-check-input'
        self.fields['ods4'].widget.attrs['class'] = 'form-check-input'
        self.fields['ods5'].widget.attrs['class'] = 'form-check-input'
        self.fields['ods6'].widget.attrs['class'] = 'form-check-input'
        self.fields['ods7'].widget.attrs['class'] = 'form-check-input'
        self.fields['ods8'].widget.attrs['class'] = 'form-check-input'
        self.fields['ods9'].widget.attrs['class'] = 'form-check-input'
        self.fields['ods10'].widget.attrs['class'] = 'form-check-input'
        self.fields['ods11'].widget.attrs['class'] = 'form-check-input'
        self.fields['ods12'].widget.attrs['class'] = 'form-check-input'
        self.fields['ods13'].widget.attrs['class'] = 'form-check-input'
        self.fields['ods14'].widget.attrs['class'] = 'form-check-input'
        self.fields['ods15'].widget.attrs['class'] = 'form-check-input'
        self.fields['ods16'].widget.attrs['class'] = 'form-check-input'
        self.fields['ods17'].widget.attrs['class'] = 'form-check-input'
        
class EniotForm(forms.ModelForm):
    seccion = forms.ChoiceField(choices=(
        ('', 'Selecciona una sección'),
        ('programa-eniot', 'Programa ENIOT'),
        ('memorias', 'Memorias'),
        ('ponencia-eventos', 'Ponencia a eventos')
    ), widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = Eniot
        fields = ['nombrePDF', 'doc_url', 'seccion', 'anio']
        labels = {
            'nombrePDF': 'Nombre del PDF',
            'doc_url': 'Documento',
            'seccion': 'Sección',
            'anio': 'Año',
        }
        widgets = {
            'nombrePDF': forms.TextInput(attrs={'class': 'form-control', 'icon_class': 'fas fa-table'}),
            'doc_url': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'anio': forms.NumberInput(attrs={'class': 'form-control', 'icon_class': 'fas fa-table'}),
        }

class EniotAlbunForm(forms.ModelForm):
    class Meta:
        model = EniotAlbun
        fields = ['nombreAlbun', 'descripcion', 'foto_url']
        widgets = {
            'nombreAlbun': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.TextInput(attrs={'class': 'form-control'}),
            'foto_url': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
        }

    def clean_foto_url(self):
        foto = self.cleaned_data.get('foto_url', False)
        if foto:
            if not isinstance(foto, str) and not foto.name.lower().endswith(('.jpg', '.jpeg', '.png', '.gif')):
                raise forms.ValidationError("Solo se permiten archivos de imagen (JPG, JPEG, PNG, GIF).")
        return foto

