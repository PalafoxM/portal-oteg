from django.forms import ModelForm, TextInput
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
            'section': TextInput(attrs = { 'placeholder': 'Ingresa una Sección'}),
            'category': TextInput(attrs = { 'placeholder': 'Ingresa una Categroia'}),            
            'type': TextInput(attrs = { 'placeholder': 'Ingresa un Tipo'}),
            'download': TextInput(attrs = { 'placeholder': 'Descarga'}),
            'name': TextInput(attrs = { 'placeholder': 'Ingresa un Nombre '}),
        }
    


class BannerForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = Banner
        fields = '__all__'
        widgets = {
            'name': TextInput(attrs = { 'placeholder': 'Ingresa una Nombre'}),
            'banner_url': TextInput(attrs = { 'placeholder': 'Ingresa un Enlace'}), 
        }
    
    
class PlacesOfInterestForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = PlacesOfInterest
        fields = '__all__'
        widgets = {
            'sitio_web': TextInput(attrs = { 'placeholder': 'Ingresa un Sitio Web'}),
            'decription': TextInput(attrs = { 'placeholder': 'Ingresa un Descripcion'}), 
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


# class ProfileForm(forms.ModelForm):
#     user = forms.CharField(widget=forms.HiddenInput, required=False)
#     exclude = ['user']

#     class Meta:
#         model = Profile
#         fields = '__all__'
#         widgets = {
#             'photo': forms.ClearableFileInput(attrs={'multiple': True}),
#             'fecha_cumple': DateInput(),
#         }


class UserForm(forms.ModelForm):

    password = forms.CharField(widget=forms.HiddenInput, required=False)
    user_permissions = forms.CharField(
        widget=forms.HiddenInput, required=False)
    is_staff = forms.CharField(widget=forms.HiddenInput, required=False)
    is_active = forms.CharField(widget=forms.HiddenInput, required=False)
    is_superuser = forms.CharField(widget=forms.HiddenInput, required=False)
    last_login = forms.CharField(widget=forms.HiddenInput, required=False)
    date_joined = forms.CharField(widget=forms.HiddenInput, required=False)
    username = forms.CharField(max_length=100, label='Nombre de Usuario')
    first_name = forms.CharField(max_length=100, label='Nombre')
    last_name = forms.CharField(widget=forms.HiddenInput, required=False)
    groups = forms.ModelMultipleChoiceField(
        queryset=Group.objects.all(), label='Roles / Permisos')
    exclude = ['password', 'user_permissions', 'is_staff', 'is_active',
               'is_superuser', 'last_login', 'date_joined', 'last_name']

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'groups')
        widgets = {
            'fecha_cumple': DateInput(),
        }


class CustomUserCreationForm(UserCreationForm):

    username = forms.CharField(max_length=100, label='Nombre de Usuario')
    first_name = forms.CharField(max_length=100, label='Nombre')
    last_name = forms.CharField(max_length=100, label='Apellido Paterno')
    apellido_materno = forms.CharField(
        max_length=100, label='Apellido Materno')
    fecha_cumple = forms.DateField(
        required=False, widget=DateInput, label='Fecha de Cumpleaños')
    direccion = forms.CharField(max_length=100, label='Dirección')
    tel = forms.CharField(max_length=100, required=False, label='Teléfono')
    email = forms.EmailField(max_length=100, label='Correo Electrónico')
    facebook = forms.CharField(max_length=100, required=False)
    twitter = forms.CharField(max_length=100, required=False)
    ciudad = forms.CharField(max_length=100, required=False)
    estado = forms.CharField(max_length=100, required=False)
    empresa_institucion = forms.CharField(
        max_length=100, required=False, label='Empresa o Institución')
    cargo = forms.CharField(max_length=100, required=False)
    licenciatura = forms.CharField(max_length=100, required=False)
    universidad_licenciatura = forms.CharField(max_length=100, required=False)
    maestria = forms.CharField(max_length=100, required=False)
    universidad_maestria = forms.CharField(max_length=100, required=False)
    doctorado = forms.CharField(max_length=100, required=False)
    universidad_doctorado = forms.CharField(max_length=100, required=False)
    photo = forms.ImageField(widget=forms.ClearableFileInput(
        attrs={'multiple': True}), label='Fotografía')
    experiencia = forms.CharField(widget=forms.Textarea, required=False)
    boletin = forms.BooleanField(
        required=False, label='Deseo recibir boletín de noticias')
    group = forms.ModelChoiceField(
        queryset=Group.objects.all(), label='Rol / Permisos')

    class Meta:
        model = User
        widgets = {
            'fecha_cumple': DateInput(),
        }

        fields = ('username', 'first_name', 'last_name', 'apellido_materno', 'fecha_cumple', 'direccion', 'tel', 'email', 'facebook', 'twitter', 'ciudad', 'estado', 'empresa_institucion',
                  'cargo', 'licenciatura', 'universidad_licenciatura', 'maestria', 'universidad_maestria', 'doctorado', 'universidad_doctorado', 'photo', 'experiencia', 'boletin', 'group')

    def save(self, commit=True):

        user = super().save(commit=False)

        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']

        if commit:
            user.save()
            self.cleaned_data['group'].user_set.add(user)

        # save fecha_cumple and direccion to Profile
        profile = Profile.objects.create(user=user,
                                         apellido_materno=self.cleaned_data['apellido_materno'],
                                         apellido_paterno=self.cleaned_data['last_name'],
                                         direccion=self.cleaned_data['direccion'],
                                         fecha_cumple=self.cleaned_data['fecha_cumple'],
                                         tel=self.cleaned_data['tel'],
                                         facebook=self.cleaned_data['facebook'],
                                         twitter=self.cleaned_data['twitter'],
                                         ciudad=self.cleaned_data['ciudad'],
                                         estado=self.cleaned_data['estado'],
                                         empresa_institucion=self.cleaned_data['empresa_institucion'],
                                         cargo=self.cleaned_data['cargo'],
                                         licenciatura=self.cleaned_data['licenciatura'],
                                         universidad_licenciatura=self.cleaned_data['universidad_licenciatura'],
                                         maestria=self.cleaned_data['maestria'],
                                         universidad_maestria=self.cleaned_data['universidad_maestria'],
                                         doctorado=self.cleaned_data['doctorado'],
                                         universidad_doctorado=self.cleaned_data['universidad_doctorado'],
                                         photo=self.cleaned_data['photo'],
                                         experiencia=self.cleaned_data['experiencia'],
                                         boletin=self.cleaned_data['boletin'],
                                         )
        profile.save()

        return user


class ImageUploadForm(forms.Form):
    image = forms.FileField()


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
        
class AlbaForm(forms.ModelForm):
    class Meta:
        model = Alba
        fields = ['archivo', 'visible']


class EventoForm(forms.ModelForm):
    class Meta:
        model = Evento
        fields = ['titulo', 'descripcion', 'fecha_inicio', 'imagen']

        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control'}),
            'fecha_inicio': forms.DateInput(attrs={'class': 'form-control'}),
            'imagen': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
        }


