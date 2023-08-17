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
    MAX_SIZE_MB = 5  # Tamaño máximo permitido en MB
    TYPE_CHOICES = (
        ('1', 'PDF'),
        ('2', 'MP3'),
        ('3', 'XLS'),
    )

    type = forms.ChoiceField(label='Tipo de Documento',choices=TYPE_CHOICES, widget=forms.Select(
        attrs={'class': 'custom-input', 'icon_class': 'fas fa-file'}))

    class Meta:
        model = Publications
        exclude = ('category', 'section', 'num_descargas')
        fields = ['type', 'name', 'doc', 'visible']
        widgets = {
            # 'type': forms.Select(attrs={'class': 'custom-input', 'icon_class': 'fas fa-file'}, choices=TYPE_CHOICES),
            'name': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-user'}),
            'doc': forms.ClearableFileInput(attrs={'class': 'custom-input-file'}),
        }
        labels = {
            'type': 'Tipo de Documento',
            'category': 'Categoría',
            'name': 'Nombre',
            'doc': 'Documento',
            'visible': 'Visible',
        }

    def clean_doc(self):
        doc = self.cleaned_data.get('doc')
        if doc:
            if doc.size > self.MAX_SIZE_MB * 1024 * 1024:
                raise forms.ValidationError(f"El documento no debe superar {self.MAX_SIZE_MB} MB de tamaño.")
        return doc



class BannerForm(ModelForm):
    MAX_SIZE_MB = 1  # Tamaño máximo permitido en MB
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = Banner
        fields = '__all__'
        widgets = {
            'name': TextInput(attrs={'placeholder': 'Ingresa una Nombre'}),
            'banner_url': TextInput(attrs={'placeholder': 'Ingresa un Enlace'}),
            'name': TextInput(attrs={'placeholder': 'Ingresa una Nombre', 'class': 'custom-input', 'icon_class': 'fas fa-search'}),
            'banner_url': TextInput(attrs={'placeholder': 'Ingresa un Enlace', 'class': 'custom-input', 'icon_class': 'fas fa-globe'}),
            'activo': CheckboxInput(attrs={'class': 'form-check-input'}),
            'imagen': ClearableFileInput(attrs={'placeholder': 'Ingresa una imagen', 'class': 'form-control-file'}),
            'subtitulo': TextInput(attrs={'placeholder': 'Ingresa un Subtitulo', 'class': 'custom-input', 'icon_class': 'fas fa-search'}),
            'titulo_pricipal': TextInput(attrs={'placeholder': 'Ingresa una Descripcion', 'class': 'custom-input', 'icon_class': 'fas fa-search'}),
        }
    
    def clean_imagen(self):
        imagen = self.cleaned_data.get('imagen', False)
        if imagen:
            #print(imagen.size)
            if imagen.size > self.MAX_SIZE_MB * 1024 * 1024:
                raise ValidationError(f"La imagen no debe superar {self.MAX_SIZE_MB} MB de tamaño.")
        return imagen


class PlacesOfInterestForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    logotipo = forms.ImageField(widget=forms.ClearableFileInput(
        attrs={'class': 'form-control-file', 'multiple': True}), label='Logotipo', required=False)
    sitio_web = forms.URLField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'icon_class': 'fas fa-table', 'placeholder': 'Ingresa un Sitio Web'}), label='Sitio Web')
    description = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'icon_class': 'fas fa-table', 'placeholder': 'Ingresa una Descripción'}), label='Descripción')

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
        fields = ['seccion', 'descripcion', 'observacion', 'imagen']
        widgets = {
            'seccion': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-search'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control'}),
            'observacion': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-search'}),
        }
        labels = {
            'seccion': 'Sección',
            'descripcion': 'Descripción',
            'observacion': 'Observación',
            'imagen': 'Imagen',
        }


class CategoriasForm(forms.ModelForm):

    class Meta:
        model = Categorias
        fields = ['nombre_categoria', 'fecha_creacion', 'seccion']

        widgets = {
            'nombre_categoria': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-search'}),
            'fecha_creacion': forms.DateInput(attrs={'class': 'form-control fecha-input', 'icon_class': 'fas fa-calendar'}),
        }
        labels = {
            'nombre_categoria': 'Nombre de la categoría',
            'fecha_creacion': 'Fecha de creación',
            'seccion': 'Sección',
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
    MAX_SIZE_MB = 1  # Tamaño máximo permitido en MB

    descripcion = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = Noticia
        fields = '__all__'
        widgets = {

            'titulo': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-search'}),
            'sitio_web': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-globe'}),
            'fecha_nota': forms.DateInput(attrs={'class': ' custom-input fecha-input', 'icon_class': 'fas fa-calendar'}),
            'autor_foto': forms.TextInput(attrs={'class': 'custom-input form-control', 'icon_class': 'fas fa-user'}),
            'autor_nota': forms.TextInput(attrs={'class': ' custom-input form-control', 'icon_class': 'fas fa-user'}),
            'fecha_recuperacion': forms.DateInput(attrs={'class': ' custom-input fecha-input', 'icon_class': 'fas fa-calendar'}),
            'imagen': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),

        }
        labels = {
            'titulo': 'Título',
            'sitio_web': 'Sitio Web',
            'fecha_nota': 'Fecha de Nota',
            'autor_foto': 'Autor de la Foto',
            'autor_nota': 'Autor de la Nota',
            'fecha_recuperacion': 'Fecha de Recuperación',
            'imagen': 'Imagen',
        }
    
    def clean_imagen(self):
        imagen = self.cleaned_data.get('imagen', False)
        if imagen:
            #print(imagen.size)
            if imagen.size > self.MAX_SIZE_MB * 1024 * 1024:
                raise ValidationError(f"La imagen no debe superar {self.MAX_SIZE_MB} MB de tamaño.")
        return imagen


class BarometroForm(forms.ModelForm):

    MAX_SIZE_MB = 1  # Tamaño máximo permitido en MB
    
    class Meta:
        model = BarometroTuristico
        fields = '__all__'
        exclude = ['num_descargas']
        widgets = {
            'nombrePDF': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-file-pdf'}),
            'yearPDF': forms.NumberInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-calendar', 'required': True}),

            'doc': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
        }
        labels = {
            'yearPDF': 'Año del PDF',
            'nombrePDF': 'Nombre del PDF',
        }
    
    def clean_doc(self):
        doc = self.cleaned_data.get('doc', False)
        if doc:
            if doc.size > self.MAX_SIZE_MB * 1024 * 1024:
                raise forms.ValidationError(f"El PDF no debe superar {self.MAX_SIZE_MB} MB de tamaño.")
        return doc



class AlbaForm(forms.ModelForm):
    class Meta:
        model = Alba
        fields = ['archivo', 'visible']


class DateInput(forms.DateInput):
    input_type = 'date'


class EventoForm(forms.ModelForm):
    MAX_SIZE_MB = 1  # Tamaño máximo permitido en MB
    
    
    TIPOS_EVENTO_CHOICES = [
        ('', 'Seleccionar'),
        ('internacionales', 'Internacionales'),
        ('nacionales', 'Nacionales'),
        ('estatales', 'Estatales'),
    ]

    tipo_evento = forms.ChoiceField(
        choices=TIPOS_EVENTO_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = Evento
        fields = ['tipo_evento', 'titulo', 'descripcion',
                  'fecha_inicio', 'fecha_fin', 'imagen']
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
            'titulo': 'Título',
            'descripcion': 'Descripción',
            'fecha_inicio': 'Fecha de inicio',
            'fecha_fin': 'Fecha de fin',
            'imagen': 'Imagen',
        }

    def clean_imagen(self):
        imagen = self.cleaned_data.get('imagen', False)
        if imagen:
            #print(imagen.size)
            if imagen.size > self.MAX_SIZE_MB * 1024 * 1024:
                raise ValidationError(f"La imagen no debe superar {self.MAX_SIZE_MB} MB de tamaño.")
        return imagen
    
   
class InventarioHoteleroForm(ModelForm):
    class Meta:
        model = InventarioHotelero
        fields = ['destino', 'fecha', 'categoria',
                  'habitaciones', 'establecimientos']
        widgets = {
            'destino': forms.TextInput(attrs={'class': 'form-control', 'icon_class': 'fas fa-search'}),
            'fecha': forms.DateInput(attrs={'class': 'form-control fecha-input', 'icon_class': 'fas fa-calendar'}),
            'categoria': forms.TextInput(attrs={'class': 'form-control', 'icon_class': 'fas fa-search'}),
            'habitaciones': forms.NumberInput(attrs={'class': 'form-control', 'icon_class': 'fas fa-table'}),
            'establecimientos': forms.NumberInput(attrs={'class': 'form-control', 'icon_class': 'fas fa-table'}),
        }
        labels = {
            'destino': 'Destino:',
            'fecha': 'Fecha:',
            'categoria': 'Categoría:',
            'habitaciones': 'Número de habitaciones:',
            'establecimientos': 'Número de establecimientos:',
        }


class CargaMasivaForm(forms.Form):
    archivo = forms.FileField(
        label='Seleccione un archivo', help_text='(xlsx, csv)')


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
            'definicion': forms.Textarea(attrs={'class': 'custom-input', 'icon_class': 'fas fa-book'}),
        }


class DataTurForm(forms.ModelForm):
    class Meta:
        model = DataTour
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['destino'].widget.attrs['class'] = 'custom-input'
        self.fields['destino'].widget.attrs['icon_class'] = 'fas fa-search'

        self.fields['fecha'].widget.attrs['class'] = 'custom-input'
        self.fields['fecha'].widget.attrs['icon_class'] = 'fas fa-calendar'

        self.fields['categoria'].widget.attrs['class'] = 'custom-input'
        self.fields['categoria'].widget.attrs['icon_class'] = 'fas fa-search'

        self.fields['cuartos_registrados_fin_periodo'].widget.attrs['class'] = 'custom-input'
        self.fields['cuartos_registrados_fin_periodo'].widget.attrs['icon_class'] = 'fas fa-table'

        self.fields['cuartos_disponibles_promedio'].widget.attrs['class'] = 'custom-input'
        self.fields['cuartos_disponibles_promedio'].widget.attrs['icon_class'] = 'fas fa-table'

        self.fields['cuartos_disponibles'].widget.attrs['class'] = 'custom-input'
        self.fields['cuartos_disponibles'].widget.attrs['icon_class'] = 'fas fa-table'

        self.fields['cuartos_ocupados'].widget.attrs['class'] = 'custom-input'
        self.fields['cuartos_ocupados'].widget.attrs['icon_class'] = 'fas fa-table'

        self.fields['cuartos_ocupados_residentes'].widget.attrs['class'] = 'custom-input'
        self.fields['cuartos_ocupados_residentes'].widget.attrs['icon_class'] = 'fas fa-table'

        self.fields['cuartos_ocupados_no_residentes'].widget.attrs['class'] = 'custom-input'
        self.fields['cuartos_ocupados_no_residentes'].widget.attrs['icon_class'] = 'fas fa-table'

        self.fields['llegadas_de_turistas'].widget.attrs['class'] = 'custom-input'
        self.fields['llegadas_de_turistas'].widget.attrs['icon_class'] = 'fas fa-table'

        self.fields['llegadas_de_turistas_residentes'].widget.attrs['class'] = 'custom-input'
        self.fields['llegadas_de_turistas_residentes'].widget.attrs['icon_class'] = 'fas fa-table'

        self.fields['llegadas_de_turistas_no_residentes'].widget.attrs['class'] = 'custom-input'
        self.fields['llegadas_de_turistas_no_residentes'].widget.attrs['icon_class'] = 'fas fa-table'

        self.fields['turistas_noche'].widget.attrs['class'] = 'custom-input'
        self.fields['turistas_noche'].widget.attrs['icon_class'] = 'fas fa-table'

        self.fields['turistas_noche_residentes'].widget.attrs['class'] = 'custom-input'
        self.fields['turistas_noche_residentes'].widget.attrs['icon_class'] = 'fas fa-table'

        self.fields['turistas_noche_no_residentes'].widget.attrs['class'] = 'custom-input'
        self.fields['turistas_noche_no_residentes'].widget.attrs['icon_class'] = 'fas fa-table'

        self.fields['porcentaje_de_ocupacion'].widget.attrs['class'] = 'custom-input'
        self.fields['porcentaje_de_ocupacion'].widget.attrs['icon_class'] = 'fas fa-table'

        self.fields['porcentaje_de_ocupacion_residentes'].widget.attrs['class'] = 'custom-input'
        self.fields['porcentaje_de_ocupacion_residentes'].widget.attrs['icon_class'] = 'fas fa-table'

        self.fields['porcentaje_de_ocupacion_no_residentes'].widget.attrs['class'] = 'custom-input'
        self.fields['porcentaje_de_ocupacion_no_residentes'].widget.attrs['icon_class'] = 'fas fa-table'

        self.fields['estadia_promedio'].widget.attrs['class'] = 'custom-input'
        self.fields['estadia_promedio'].widget.attrs['icon_class'] = 'fas fa-table'

        self.fields['estadia_promedio_residentes'].widget.attrs['class'] = 'custom-input'
        self.fields['estadia_promedio_residentes'].widget.attrs['icon_class'] = 'fas fa-table'

        self.fields['estadia_promedio_no_residentes'].widget.attrs['class'] = 'custom-input'
        self.fields['estadia_promedio_no_residentes'].widget.attrs['icon_class'] = 'fas fa-table'

        self.fields['densidad_de_ocupacion'].widget.attrs['class'] = 'custom-input'
        self.fields['densidad_de_ocupacion'].widget.attrs['icon_class'] = 'fas fa-table'

        self.fields['densidad_de_ocupacion_residentes'].widget.attrs['class'] = 'custom-input'
        self.fields['densidad_de_ocupacion_residentes'].widget.attrs['icon_class'] = 'fas fa-table'

        self.fields['densidad_de_ocupacion_no_residentes'].widget.attrs['class'] = 'custom-input'
        self.fields['densidad_de_ocupacion_no_residentes'].widget.attrs['icon_class'] = 'fas fa-table'


class GastoDerramaForm (forms.ModelForm):
    class Meta:
        model = GastoDerrama
        fields =  '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['gasto_diario_prom'].widget.attrs['class'] = 'custom-input'
        self.fields['gasto_diario_prom'].widget.attrs['icon_class'] = 'fas fa-search'

        self.fields['ano'].widget.attrs['class'] = 'custom-input'
        self.fields['ano'].widget.attrs['icon_class'] = 'fas fa-calendar'

        self.fields['tipo_visitante'].widget.attrs['class'] = 'custom-input'
        self.fields['tipo_visitante'].widget.attrs['icon_class'] = 'fas fa-calendar'

        self.fields['destino'].widget.attrs['class'] = 'custom-input'
        self.fields['destino'].widget.attrs['icon_class'] = 'fas fa-calendar'

        self.fields['participacion_en_hospedaje'].widget.attrs['class'] = 'custom-input'
        self.fields['participacion_en_hospedaje'].widget.attrs['icon_class'] = 'fas fa-calendar'

        self.fields['estadia_promedio'].widget.attrs['class'] = 'custom-input'
        self.fields['estadia_promedio'].widget.attrs['icon_class'] = 'fas fa-calendar'



class OtrosAnualesForm (forms.ModelForm):
    class Meta:
        model = otros_anuales
        fields = '__all__'

        widgets = {
            'ano': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-search'}),
            'PIB_sector_72': forms.Textarea(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'PIB_actividades_terciarias': forms.Textarea(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'basura_generada_persona_diaria_Kg': forms.Textarea(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
        }


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
    origen_visitante = forms.ChoiceField(
        choices=ORIGEN_CHOICES, required=True)

    class Meta:
        model = zonas_arqueologicas_museos
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['destino'].widget.attrs['class'] = 'custom-input'
        self.fields['destino'].widget.attrs['icon_class'] = 'fas fa-search'

        self.fields['fecha'].widget.attrs['class'] = 'custom-input'
        self.fields['fecha'].widget.attrs['icon_class'] = 'fas fa-calendar'

        self.fields['tipo'].widget.attrs['class'] = 'custom-input'
        self.fields['tipo'].widget.attrs['icon_class'] = 'fas fa-sort-numeric-up'

        self.fields['nombre'].widget.attrs['class'] = 'custom-input'
        self.fields['nombre'].widget.attrs['icon_class'] = 'fas fa-table'

        self.fields['visitantes'].widget.attrs['class'] = 'custom-input'
        self.fields['visitantes'].widget.attrs['icon_class'] = 'fas fa-table'

        self.fields['origen_visitante'].widget.attrs['class'] = 'custom-input'
        self.fields['origen_visitante'].widget.attrs['icon_class'] = 'fas fa-table'


class ZonasArqueologicasMuseosForm_edit (forms.ModelForm):
    TIPO_CHOICES = (
        ('museo', 'Museo'),
        ('zona arqueologica', 'Zona Arqueológica'),
    )
    tipo = forms.ChoiceField(choices=TIPO_CHOICES, required=False)


    
    ORIGEN_CHOICES = (
        ('nacional', 'Nacional'),
        ('extranjero', 'Extranjero'),
    )
    origen_visitante = forms.ChoiceField(
        choices=ORIGEN_CHOICES, required=True)



    class Meta:
        model = zonas_arqueologicas_museos
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['destino'].widget.attrs['class'] = 'custom-input'
        self.fields['destino'].widget.attrs['icon_class'] = 'fas fa-search'

        self.fields['fecha'].widget.attrs['class'] = 'custom-input'
        self.fields['fecha'].widget.attrs['icon_class'] = 'fas fa-calendar'

        self.fields['tipo'].widget.attrs['class'] = 'custom-input'
        self.fields['tipo'].widget.attrs['icon_class'] = 'fas fa-sort-numeric-up'

        self.fields['nombre'].widget.attrs['class'] = 'custom-input'
        self.fields['nombre'].widget.attrs['icon_class'] = 'fas fa-table'

        self.fields['visitantes'].widget.attrs['class'] = 'custom-input'
        self.fields['visitantes'].widget.attrs['icon_class'] = 'fas fa-table'

        self.fields['origen_visitante'].widget.attrs['class'] = 'custom-input'
        self.fields['origen_visitante'].widget.attrs['icon_class'] = 'fas fa-table'


class SensivilizacionForm (forms.ModelForm):
    class Meta:
        model = Sensivilizacion
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['destino'].widget.attrs['class'] = 'custom-input'
        self.fields['destino'].widget.attrs['icon_class'] = 'fas fa-search'

        self.fields['fecha'].widget.attrs['class'] = 'custom-input'
        self.fields['fecha'].widget.attrs['icon_class'] = 'fas fa-calendar'

        self.fields['participantes'].widget.attrs['class'] = 'custom-input'
        self.fields['participantes'].widget.attrs['icon_class'] = 'fas fa-sort-numeric-up'

        self.fields['accion_de_sensibilizacion'].widget.attrs['class'] = 'custom-input'
        self.fields['accion_de_sensibilizacion'].widget.attrs['icon_class'] = 'fas fa-table'


class CertificacionForm (forms.ModelForm):
    class Meta:
        model = Certificacion
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['destino'].widget.attrs['class'] = 'custom-input'
        self.fields['destino'].widget.attrs['icon_class'] = 'fas fa-search'

        self.fields['fecha'].widget.attrs['class'] = 'custom-input'
        self.fields['fecha'].widget.attrs['icon_class'] = 'fas fa-calendar'

        self.fields['tipo_de_certificacion'].widget.attrs['class'] = 'custom-input'
        self.fields['tipo_de_certificacion'].widget.attrs['icon_class'] = 'fas fa-search'

        self.fields['empresas_certificadas'].widget.attrs['class'] = 'custom-input'
        self.fields['empresas_certificadas'].widget.attrs['icon_class'] = 'fas fa-table'


class InversionPublicaForm(forms.ModelForm):
    class Meta:
        model = InversionPublica
        fields = ['fecha', 'destino', 'nombre_de_la_obra', 'monto_de_inversion_municipal',
                  'monto_de_inversion_estatal', 'monto_de_inversion_federal', 'monto_total']

    def __init__(self, *args, **kwargs):
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
        fields = ['entidad', 'fecha', 'categoria',
                  'habitaciones', 'establecimientos']
        labels = {
            'entidad': 'Entidad:',
            'fecha': 'Fecha:',
            'categoria': 'Categoría:',
            'habitaciones': 'Número de habitaciones:',
            'establecimientos': 'Número de establecimientos:',
        }

    def __init__(self, *args, **kwargs):
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
            'fecha': forms.DateInput(attrs={'class': 'form-control fecha-input', 'icon_class': 'fas fa-calendar'}),
            'destino': forms.TextInput(attrs={'class': 'form-control', 'icon_class': 'fas fa-search'}),
            'calidad_del_aire': forms.TextInput(attrs={'class': 'form-control', 'icon_class': 'fas fa-table'}),
        },
        labels = {
            'fecha': 'Fecha:',
            'destino': 'Destino:',
            'calidad_del_aire': 'Calidad del aire:',
        }


class ProyectoInversionForm(forms.ModelForm):
    class Meta:
        model = ProyectoInversion
        fields = '__all__'
        labels = {
            'destino': 'Destino:',
            'nombre_del_proyecto': 'Nombre del proyecto:',
            'promotor_del_proyecto': 'Promotor del proyecto:',
            'referencia_de_ubicacion': 'Referencia de ubicación:',
            'zona_turistica': 'Zona turística:',
            'giro': 'Giro:',
            'habitaciones': 'Habitaciones:',
            'empleos_permanentes': 'Empleos permanentes:',
            'empleos_temporales': 'Empleos temporales:',
            'tipo_de_inversion': 'Tipo de inversión:',
            'origen_de_inversion': 'Origen de inversión:',
            'estatus': 'Estatus:',
            'fecha_de_inicio_de_obra': 'Fecha de inicio de obra:',
            'fecha_de_conclusion_de_obra': 'Fecha de conclusión de obra:',
            'fecha_de_apertura': 'Fecha de apertura:',
            'monto_comprometido_del_proyecto_mxn': 'Monto comprometido del proyecto (MXN):',
            'plazo': 'Plazo:',
            'personas_beneficiadas_con_el_proyecto': 'Personas beneficiadas con el proyecto:',
            'datos_de_contacto': 'Datos de contacto:',
        }
        widgets = {
            'destino': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Destino', 'icon_class': 'fas fa-search'}),
            'fecha': forms.DateInput(attrs={'class': 'form-control fecha-input', 'placeholder': 'Fecha', 'icon_class': 'fas fa-calendar'}),
            'calidad_del_aire': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Calidad del aire', 'icon_class': 'fas fa-table'}),
            'nombre_del_proyecto': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre del proyecto', 'icon_class': 'fas fa-table'}),
            'promotor_del_proyecto': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Promotor del proyecto', 'icon_class': 'fas fa-table'}),
            'referencia_de_ubicacion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Referencia de ubicación', 'icon_class': 'fas fa-table'}),
            'zona_turistica': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Zona turística', 'icon_class': 'fas fa-table'}),
            'giro': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Giro', 'icon_class': 'fas fa-table'}),
            'habitaciones': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Habitaciones', 'icon_class': 'fas fa-table'}),
            'empleos_permanentes': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Empleos permanentes', 'icon_class': 'fas fa-table'}),
            'empleos_temporales': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Empleos temporales', 'icon_class': 'fas fa-table'}),
            'tipo_de_inversion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tipo de inversión', 'icon_class': 'fas fa-table'}),
            'origen_de_inversion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Origen de inversión', 'icon_class': 'fas fa-table'}),
            'estatus': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Estatus', 'icon_class': 'fas fa-table'}),
            'fecha_de_inicio_de_obra': forms.DateInput(attrs={'class': 'form-control fecha-input', 'placeholder': 'Fecha de inicio de obra', 'icon_class': 'fas fa-calendar'}),
            'fecha_de_conclusion_de_obra': forms.DateInput(attrs={'class': 'form-control fecha-input', 'placeholder': 'Fecha de conclusión de obra', 'icon_class': 'fas fa-calendar'}),
            'fecha_de_apertura': forms.DateInput(attrs={'class': 'form-control fecha-input', 'placeholder': 'Fecha de apertura', 'icon_class': 'fas fa-calendar'}),
            'monto_comprometido_del_proyecto_mxn': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Monto comprometido del proyecto (MXN)', 'icon_class': 'fas fa-table'}),
            'plazo': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Plazo', 'icon_class': 'fas fa-table'}),
            'personas_beneficiadas_con_el_proyecto': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Personas beneficiadas con el proyecto', 'icon_class': 'fas fa-table'}),
            'datos_de_contacto': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Datos de contacto', 'icon_class': 'fas fa-table'}),
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
            'destino_aeropuerto': forms.TextInput(attrs={'class': 'custom-input' , 'icon_class': 'fas fa-search'}),
            'destino_aeropuerto_id': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'})
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
        fields = ['destino', 'nombre_del_proyecto',
                  'fecha', 'monto_ejecutado', 'avance_proyecto']

        widgets = {
            'destino': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Destino', 'icon_class': 'fas fa-search'}),
            'fecha': forms.DateInput(attrs={'class': 'form-control fecha-input', 'placeholder': 'Fecha', 'icon_class': 'fas fa-calendar'}),
            'monto_ejecutado': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Monto Ejecutado', 'icon_class': 'fas fa-dollar-sign'}),
            'avance_proyecto': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Avance Proyecto', 'icon_class': 'fas fa-percent'}),
            'nombre_del_proyecto': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre del Proyecto', 'icon_class': 'fas fa-table'}),
        }


class InversionPrivadaEditForm(forms.ModelForm):
    class Meta:
        model = inversion_privada
        fields = ['id_del_proyecto', 'nombre_del_proyecto',
                  'destino', 'fecha', 'monto_ejecutado', 'avance_proyecto']

        widgets = {
            'id_del_proyecto': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'ID del Proyecto', 'icon_class': 'fas fa-table'}),
            'destino': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Destino', 'icon_class': 'fas fa-search'}),
            'fecha': forms.DateInput(attrs={'class': 'form-control fecha-input', 'placeholder': 'Fecha', 'icon_class': 'fas fa-calendar'}),
            'monto_ejecutado': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Monto Ejecutado', 'icon_class': 'fas fa-dollar-sign'}),
            'avance_proyecto': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Avance Proyecto', 'icon_class': 'fas fa-percent'}),
            'nombre_del_proyecto': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre del Proyecto', 'icon_class': 'fas fa-table'}),
        }


class EmpleoForm (forms.ModelForm):
    class Meta:
        model = empleo
        fields = '__all__'

        widgets = {
            'fecha_inicio': forms.DateInput(attrs={'class': 'form-control fecha-input', 'placeholder': 'Fecha', 'icon_class': 'fas fa-calendar'}),
            'fecha_fin': forms.NumberInput(attrs={'class': 'custom-input fecha-input', 'icon_class': 'fas fa-calendar'}),
            'hombres_empleados_gto': forms.NumberInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'mujeres_empleadas_gto': forms.NumberInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'hombres_empleados_sec_72_gto': forms.NumberInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'mujeres_empleadas_sec_72_gto': forms.NumberInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'hombres_empleados_sec_72_nac': forms.NumberInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'mujeres_empleadas_sec_72_nac': forms.NumberInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
        }


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

        widgets = {
            'destino': forms.DateInput(attrs={'class': 'custom-input','icon_class': 'fas fa-search'}),
            'entidad': forms.NumberInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),

        }


class AirbnbForm (forms.ModelForm):
    class Meta:
        model = Airbnb
        fields = '__all__'

        widgets = {
            'fecha_inicio': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-calendar'}),
            'fecha_fin': forms.DateInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-calendar'}),
            'destino': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-search'}),
            'propiedad_renta': forms.NumberInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'porcentaje_ocupacion': forms.NumberInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'tarifa_promedio': forms.NumberInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'fecha_actualizacion': forms.NumberInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
        }


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
            'pasajeros_aeropuerto_gto': forms.NumberInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'pasajeros_nacionales': forms.NumberInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'pasajeros_internacionales': forms.NumberInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'fecha': forms.DateInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-calendar'}),
            'vuelos': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
        }


class AerolineaForm(forms.ModelForm):

    TIPOS_EVENTO_CHOICES = [
        ('Internacional', 'Internacional'),
        ('Nacional', 'Nacional'),
    ]

    tipo_aerolinea = forms.ChoiceField(
        choices=TIPOS_EVENTO_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = Aerolinea
        fields = '__all__'
        labels = {
            'fecha': 'Fecha',
            'destino_aeropuerto': 'Destino Aeropuerto',
            'destino_aeropuerto_id': 'ID Destino Aeropuerto',
            'tipo_aerolinea': 'Tipo de Aerolínea',
            'codigo_aerolinea': 'Código de Aerolínea',
            'nombre_aerolinea': 'Nombre de la Aerolínea',
        }
        widgets = {
            'fecha': forms.DateInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-calendar'}),
            'destino_aeropuerto': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-search'}),
            'destino_aeropuerto_id': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'tipo_aerolinea': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'codigo_aerolinea': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'nombre_aerolinea': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
        }


class ParticipacionOrigenForm (forms.ModelForm):
    class Meta:
        model = ParticipacionOrigen
        fields = '__all__'
        labels = {
            'anio': 'Año',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['ano'].widget.attrs['class'] = 'custom-input'
        self.fields['ano'].widget.attrs['icon_class'] = 'fas fa-calendar'
        self.fields['destino'].widget.attrs['class'] = 'custom-input'
        self.fields['destino'].widget.attrs['icon_class'] = 'fas fa-search'
        self.fields['part_visitantes_int'].widget.attrs['class'] = 'custom-input'
        self.fields['part_visitantes_int'].widget.attrs['icon_class'] = 'fas fa-search'

        self.fields['part_visitantes_nac'].widget.attrs['class'] = 'custom-input'
        self.fields['part_visitantes_nac'].widget.attrs['icon_class'] = 'fas fa-search'
        self.fields['part_visitantes_est'].widget.attrs['class'] = 'custom-input'
        self.fields['part_visitantes_est'].widget.attrs['icon_class'] = 'fas fa-search'


class FuenteInfoEntornoNForm (forms.ModelForm):
    class Meta:
        model = FuenteInfoEntornoN
        fields = '__all__'

        widgets = {
            'entidad': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-search'}),
            'fecha': forms.DateInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-calendar'}),
            'cuartos_disponibles_promedio': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'cuartos_disponibles': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'cuartos_ocupados': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'cuartos_ocupados_nacionales': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'cuartos_ocupados_extranjeros': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'cuartos_ocupados_sin_clasificar': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'llegada_de_turistas': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'llegada_de_turistas_nacionales': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'llegada_de_turistas_extranjeros': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'turistas_noche': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'turistas_noche_nacionales': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'turistas_noche_extranjeros': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'porcentaje_de_ocupacion': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'porcentaje_de_ocupacion_nacionales': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'porcentaje_de_ocupacion_extranjeros': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'porcentaje_de_ocupacion_sin_clasificar': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'densidad': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'densidad_nacionales': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'densidad_extranjeros': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'estadia_promedio': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'estadia_promedio_nacionales': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'estadia_promedio_extranjeros': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),


        }


class FuenteInfoPerfilVisitanteEventoForm (forms.ModelForm):
    class Meta:
        model = FuenteInfoPerfilVisitanteEvento
        fields = '__all__'

        labels = {
            'ano': 'Año',
            'codigo_encuesta_ano': 'Código de encuesta año',
        }

        widgets = {
            'ano': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-calendar'}),
            'folio': forms.DateInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'fecha': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-calendar'}),
            'destino': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'nombre_evento': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'segmento': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'tipo_participante': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'residencia': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'tipo_asistente': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'municipio': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'estado': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'pais': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'origen': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'tipo_hospedaje': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'tipo_visitante': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'grupo_viaje': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'acompanantes_maxmin': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'nps_evento': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'nps_evento_categoria': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'edad': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'nse': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'sexo': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'codigo_encuesta_ano': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
        }


class FuenteInfoPerfilVisitanteDestinoForm (forms.ModelForm):

    class Meta:
        model = FuenteInfoPerfilVisitanteDestino
        fields = '__all__'

        labels = {
            'ano': 'Año',
            'codigo_encuesta_ano': 'Código de encuesta año',
        }

        widgets = {
            'ano': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-calendar'}),
            'folio': forms.DateInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'fecha': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-calendar'}),
            'herramienta': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),

            'temporada': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'destino': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'residencia': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),

            'tipo_asistente': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'municipio': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'estado': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'pais': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'origen': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'motivo_visita': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),

            'motivo_visita_otro': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'grupo_viaje': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'segmento': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'tipo_hospedaje': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),

            'tipo_visitante': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'estadia_dias': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'estadia_hrs': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'acompanantes': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'acompanantes_maxmin': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'medio_transporte_edo': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'tiene_fam': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'visita_fam': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),


            'sat_hospedaje': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'sat_ayb': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'sat_atractivos': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),

            'sat_tours': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'sat_central': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'sat_aeropuerto': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),

            'sat_carretera': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'sat_infotur': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),


            'sat_estacionamiento': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'sat_hospitalidad': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),


            'sat_seguridad': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),

            'sat_experiencia': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'sat_accesibilidad': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'sat_senaletica': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),


            'sat_transporte': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'sat_limpieza': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'sat_eventos': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),


            'sat_protocolos': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'sat_precios': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'recomendacion_destino': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),



            # retorno_destino = models.CharField(max_length=256, verbose_name='Retorno al destino')
            # nps_destino = models.FloatField(verbose_name='NPS del destino')
            # nps_destino_categoria = models.CharField(max_length=256, verbose_name='Categoría NPS del destino')

            # nps_hotel = models.FloatField(verbose_name='NPS del hotel')
            # nps_ayb = models.FloatField(verbose_name='NPS de alimentos y bebidas')
            # nps_atractivos = models.FloatField(verbose_name='NPS de atractivos turísticos')

            # nps_tours = models.FloatField(verbose_name='NPS de tours o actividades')
            # vio_escucho_noticias = models.CharField(max_length=256, verbose_name='Vio o escuchó noticias del destino')
            # impacto_noticias = models.CharField(max_length=256, verbose_name='Impacto de las noticias en la visita')

            # identifico_practicas_sust = models.CharField(max_length=256, verbose_name='Identificación de prácticas sustentables')
            # edad = models.FloatField(verbose_name='Edad')
            # nse = models.CharField(max_length=256, verbose_name='NSE (Nivel Socioeconómico)')

            # sexo = models.CharField(max_length=256, verbose_name='Sexo')
            # proposito_visita_destino_estado = models.CharField(max_length=256, verbose_name='Propósito de la visita al destino o estado')
            # codigo_encuesta_ano = models.CharField(max_length=256, verbose_name='Código de encuesta del año')

            'retorno_destino': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'nps_destino': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'nps_destino_categoria': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),

            'nps_hotel': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'nps_ayb': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'nps_atractivos': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'nps_tours': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'vio_escucho_noticias': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'impacto_noticias': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'identifico_practicas_sust': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'edad': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'nse': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'sexo': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),

            'proposito_visita_destino_estado': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'codigo_encuesta_ano': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),


            





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

    class Meta:
        model = Pasajeros_Ent_Nac
        fields = '__all__'


        widgets = {
            'aereopuerto': forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-calendar'}),
        # entidad = models.CharField(max_length=256, verbose_name='Entidad')
        # ano = models.IntegerField(verbose_name='Año')
        # nacionales = models.IntegerField(verbose_name='Pasajeros Nacionales')
        # internacionales = models.IntegerField(verbose_name='Pasajeros Internacionales')
        # regulares = models.IntegerField(verbose_name='Pasajeros Regulares')
        # nacionales_regulares = models.IntegerField(verbose_name='Pasajeros Nacionales Regulares')
        # internacionales_regulares = models.IntegerField(verbose_name='Pasajeros Internacionales Regulares')
        # charters = models.IntegerField(verbose_name='Pasajeros Charters')
        # charters_nacionales = models.IntegerField(verbose_name='Pasajeros Charters Nacionales')
        # charters_internacionales = models.IntegerField(verbose_name='Pasajeros Charters Internacionales')
            'entidad' : forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-search'}),
            'ano' : forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'nacionales' : forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'internacionales' : forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'regulares' : forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'nacionales_regulares' : forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'internacionales_regulares' : forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'charters' : forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'charters_nacionales' : forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
            'charters_internacionales' : forms.TextInput(attrs={'class': 'custom-input', 'icon_class': 'fas fa-table'}),
        }



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

# Direcctorio Turistico


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

    def __init__(self, *args, **kwargs):
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

    def __init__(self, *args, **kwargs):
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
            'depende_de_hotel_o_restaurante': 'Depende de hotel o restaurante',
            'no_de_salones': 'no de salones',
            'capacidad_maxima': 'Capacidad maxima',
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

    seccion = forms.ChoiceField(choices=TYPE_CHOICES, widget=forms.Select(
        attrs={'class': 'custom-input', 'icon_class': 'fas fa-file'}))
    url = forms.URLField(widget=forms.URLInput(
        attrs={'class': 'custom-input', 'icon_class': 'fas fa-globe'}))
    activo = forms.BooleanField(required=False, widget=forms.CheckboxInput(
        attrs={'class': 'form-check-input'}))

    class Meta:
        model = Encuesta
        fields = '__all__'
        labels = {
            'seccion': 'Sección',
            'url': 'URL',
            'activo': 'Activo',
        }


class ReporteMensualForm(forms.ModelForm):
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

    mes = forms.ChoiceField(choices=MES_CHOICES, widget=forms.Select(
        attrs={'class': 'custom-input', 'icon_class': 'fas fa-calendar'}))

    class Meta:
        model = Reportes_Mensuales
        fields = '__all__'
        exclude = ['num_descargas']

        labels = {'ano': 'Año', 'mes': 'Mes', 'titulo': 'Título'}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['ano'].widget.attrs['class'] = 'custom-input'
        self.fields['ano'].widget.attrs['icon_class'] = 'fas fa-calendar'

        self.fields['titulo'].widget.attrs['class'] = 'custom-input'
        self.fields['titulo'].widget.attrs['icon_class'] = 'fas fa-search'


class ReportsForm(forms.ModelForm):
    MAX_SIZE_MB = 1  # Tamaño máximo permitido en MB

    descripcion = forms.CharField(widget=CKEditorWidget())
    class Meta:
        model = Report
        fields = '__all__'
        exclude = ['dimension']

        labels = {
            'nomenclatura': 'Título Corto',
            'titulo': 'Título',
            'descripcion': 'Descripción',}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['titulo'].widget.attrs['class'] = 'custom-input'
        self.fields['titulo'].widget.attrs['icon_class'] = 'fas fa-search'
        self.fields['nomenclatura'].widget.attrs['class'] = 'custom-input'
        self.fields['nomenclatura'].widget.attrs['icon_class'] = 'fas fa-search'
        self.fields['iframe'].widget.attrs['class'] = 'custom-input'
        self.fields['iframe'].widget.attrs['icon_class'] = 'fas fa-search'
        self.fields['ods1'].widget.attrs['class'] = 'form-check-input'
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
    MAX_SIZE_MB = 1  # Tamaño máximo permitido en MB
    seccion = forms.ChoiceField(choices=(
        ('', 'Selecciona una sección'),
        ('programa-eniot', 'Programa ENIOT'),
        ('memorias', 'Memorias'),
        ('ponencia-eventos', 'Ponencia a eventos')
    ), widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = Eniot
        fields = ['nombrePDF', 'seccion', 'anio', 'doc_url',]
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

    def clean_imagen(self):
        imagen = self.cleaned_data.get('doc_url', False)
        if imagen:
            #print(imagen.size)
            if imagen.size > self.MAX_SIZE_MB * 1024 * 1024:
                raise ValidationError(f"La imagen no debe superar {self.MAX_SIZE_MB} MB de tamaño.")
        return imagen

class EniotAlbunForm(forms.ModelForm):
    MAX_SIZE_MB = 1  # Tamaño máximo permitido en MB
    class Meta:
        model = EniotAlbun
        fields = ['nombreAlbun', 'descripcion', 'foto_url']
        widgets = {
            'nombreAlbun': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.TextInput(attrs={'class': 'form-control'}),
            'foto_url': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
        }

        labels = {
            'nombreAlbun': 'Nombre del Álbum',
            'descripcion': 'Descripción',
            'foto_url': 'Foto',
        }
    
    def clean_imagen(self):
        imagen = self.cleaned_data.get('foto_url', False)
        if imagen:
            #print(imagen.size)
            if imagen.size > self.MAX_SIZE_MB * 1024 * 1024:
                raise ValidationError(f"La imagen no debe superar {self.MAX_SIZE_MB} MB de tamaño.")
        return imagen

    def clean_foto_url(self):
        foto = self.cleaned_data.get('foto_url', False)
        if foto:
            if not isinstance(foto, str) and not foto.name.lower().endswith(('.jpg', '.jpeg', '.png', '.gif')):
                raise forms.ValidationError(
                    "Solo se permiten archivos de imagen (JPG, JPEG, PNG, GIF).")
        return foto
