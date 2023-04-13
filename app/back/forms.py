from django.forms import ModelForm, TextInput, ClearableFileInput, CheckboxInput
from .models import *
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from django.contrib.auth.models import User, Group

class PublicationForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = Publications
        fields = '__all__'
        widgets = {
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


class CategoriasForm(forms.ModelForm):
    seccion = forms.IntegerField(widget=forms.HiddenInput, required=False)
    fecha_creacion = forms.DateField(required=False, widget=DateInput)

    class Meta:
        model = Categorias
        fields = ['nombre_categoria', 'fecha_creacion',
                  'publicacion', 'visible', 'seccion']

class NoticiaForm(ModelForm):
    
    class Meta:
        model = Noticia
        fields = ['titulo', 'descripcion', 'sitio_web',
                  'imagen', 'fecha_nota', 'autor_foto', 'autor_nota', 'fecha_recuperacion']
        widgets = {

            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control'}),
            'sitio_web': forms.TextInput(attrs={'class': 'form-control'}),
            'imagen': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'fecha_nota': forms.DateInput(attrs={'class': 'form-control'}),
            'autor_foto': forms.TextInput(attrs={'class': 'form-control'}),
            'autor_nota': forms.TextInput(attrs={'class': 'form-control'}),
            'fecha_recuperacion': forms.DateInput(attrs={'class': 'form-control'}),

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
