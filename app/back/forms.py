from django.forms import ModelForm, TextInput, ClearableFileInput, CheckboxInput
from .models import *
from web.models import *
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from django.contrib.auth.models import User, Group
from ckeditor.widgets import CKEditorWidget

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
    class Meta:
        model = Publications
        exclude = ('category', 'section', 'num_descargas')
        fields = '__all__'
        widgets = {

            'type': forms.Select(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'url': forms.TextInput(attrs={'class': 'form-control'}),

            'section': TextInput(attrs = { 'placeholder': 'Ingresa una Sección', 'class': 'form-control'}),
            'category': TextInput(attrs = { 'placeholder': 'Ingresa una Categroia', 'class': 'form-control'}),            
            'type': TextInput(attrs = { 'placeholder': 'Ingresa un Tipo', 'class': 'form-control'}),
            'download': TextInput(attrs = { 'placeholder': 'Descarga', 'class': 'form-control'}),
            'name': TextInput(attrs = { 'placeholder': 'Ingresa un Nombre ', 'class': 'form-control'}),
            'fiel': ClearableFileInput(attrs = { 'placeholder': 'Ingresa una imagen', 'class': 'form-control-file'}), 
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
            'name': TextInput(attrs = { 'placeholder': 'Ingresa una Nombre', 'class': 'form-control'}),
            'banner_url': TextInput(attrs = { 'placeholder': 'Ingresa un Enlace', 'class': 'form-control'}), 
            'publication': CheckboxInput(attrs = { 'placeholder': 'Ingresa una Publicación', 'class': 'form-control'}), 
            'imagen': ClearableFileInput(attrs = { 'placeholder': 'Ingresa una imagen', 'class': 'form-control-file'}), 
        }


class PlacesOfInterestForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = PlacesOfInterest
        fields = '__all__'
        widgets = {
            'sitio_web': TextInput(attrs={'placeholder': 'Ingresa un Sitio Web'}),
            'decription': TextInput(attrs={'placeholder': 'Ingresa un Descripcion'}),
            'sitio_web': TextInput(attrs = { 'placeholder': 'Ingresa un Sitio Web', 'class': 'form-control'}),
            'decription': TextInput(attrs = { 'placeholder': 'Ingresa un Descripcion', 'class': 'form-control'}), 
        }


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
        fields = ['seccion', 'descripcion', 'observacion']
        widgets = {
            'seccion': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control'}),
            'observacion': forms.TextInput(attrs={'class': 'form-control'}),
        }


class CategoriasForm(forms.ModelForm):

    class Meta:
        model = Categorias
        fields = ['nombre_categoria', 'fecha_creacion',
                  'publicacion', 'visible', 'seccion']

        widgets = {
            'nombre_categoria': forms.TextInput(attrs={'class': 'form-control'}),
            'fecha_creacion': forms.DateInput(attrs={'class': 'form-control fecha-input'}),
            'publicacion': forms.CheckboxInput(attrs={'class': 'form-control'}),
            'visible': forms.CheckboxInput(attrs={'class': 'form-control'}),
            'seccion': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        pk = kwargs.pop('pk', None)
        super().__init__(*args, **kwargs)
        if pk:
            seccion = SeccionesCentroDocumental.objects.get(pk=pk)
            self.fields['seccion'].initial = seccion
            self.fields['seccion'].widget = forms.HiddenInput()


class NoticiaForm(ModelForm):

    descripcion = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = Noticia
        fields = ['titulo', 'descripcion', 'sitio_web',
                  'imagen', 'fecha_nota', 'autor_foto', 'autor_nota', 'fecha_recuperacion']
        widgets = {

            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'sitio_web': forms.TextInput(attrs={'class': 'form-control'}),
            'imagen': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'fecha_nota': forms.DateInput(attrs={'class': 'form-control fecha-input'}),
            'autor_foto': forms.TextInput(attrs={'class': 'form-control'}),
            'autor_nota': forms.TextInput(attrs={'class': 'form-control'}),
            'fecha_recuperacion': forms.DateInput(attrs={'class': 'form-control fecha-input'}),

        }


class BarometroForm(forms.ModelForm):
    class Meta:
        model = BarometroTuristico
        fields = ['semestre', 'nombrePDF', 'url', 'yearPDF']
        widgets = {
            'semestre': forms.NumberInput(attrs={'class': 'form-control', 'required': True}),
            'nombrePDF': forms.TextInput(attrs={'class': 'form-control'}),
            'url': forms.URLInput(attrs={'class': 'form-control'}),
            'yearPDF': forms.NumberInput(attrs={'class': 'form-control', 'required': True}),
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
            'palabra': forms.TextInput(attrs={'class': 'form-control'}),
            'definicion': forms.TextInput(attrs={'class': 'form-control'}),
        }


class DataTurForm(forms.ModelForm):
    class Meta:
        model = DataTour
        fields = '__all__'

class GastoDerramaForm (forms.ModelForm):
    class Meta:
        model = GastoDerrama
        fields = ['anio', 'categoria', 'destino', 'gasto_diario_promedio','participacion','estadia_promedio']


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


class SensibilizacionForm (forms.ModelForm):
    class Meta:
        model = Sesibilizacion
        fields = '__all__'  


class CertificacionForm (forms.ModelForm):
    class Meta:
        model = Certificacion
        fields = '__all__'


class InversionPublicaForm(forms.ModelForm):
    class Meta:
        model = InversionPublica
        fields = ['fecha', 'destino', 'nombre_de_la_obra', 'monto_de_inversion_municipal', 'monto_de_inversion_estatal', 'monto_de_inversion_federal', 'monto_total']
        widgets = {
            'fecha': forms.DateInput(attrs={'class': 'form-control fecha-input'}),
            'destino': forms.TextInput(attrs={'class': 'form-control'}),
            'nombre_de_la_obra': forms.TextInput(attrs={'class': 'form-control'}),
            'monto_de_inversion_municipal': forms.NumberInput(attrs={'class': 'form-control'}),
            'monto_de_inversion_estatal': forms.NumberInput(attrs={'class': 'form-control'}),
            'monto_de_inversion_federal': forms.NumberInput(attrs={'class': 'form-control'}),
            'monto_total': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class InventarioHoteleroEntNacForm(ModelForm):
    class Meta:
        model = InventarioHoteleroEntNac
        fields = ['destino', 'fecha', 'categoria', 'habitaciones', 'establecimientos']
        widgets = {
            'destino': forms.TextInput(attrs={'class': 'form-control'}),
            'fecha': forms.DateInput(attrs={'class': 'form-control fecha-input'}),
            'categoria': forms.TextInput(attrs={'class': 'form-control'}),
            'habitaciones': forms.NumberInput(attrs={'class': 'form-control'}),
            'establecimientos': forms.NumberInput(attrs={'class': 'form-control'}),
        }

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