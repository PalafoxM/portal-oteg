from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Profile
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from django.contrib.auth.models import User, Group
from django.db import models
from django.forms import formset_factory
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from django.contrib.auth.models import Group
from django.core.validators import RegexValidator
from django.core.files.base import ContentFile
from django.forms import PasswordInput



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


class ProfileForm(forms.ModelForm):
    user = forms.CharField(widget=forms.HiddenInput, required=False)
    exclude = ['user']

    class Meta:
        model = Profile
        fields = '__all__'
        widgets = {
            'photo': forms.ClearableFileInput(attrs={'multiple': True}),
            'fecha_cumple': DateInput(),
        }


class UserForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['autofocus'] = True

    class Meta:
        model = User
        fields = 'first_name', 'last_name', 'email', 'username', 'password', 'groups'
        widgets = {
            'first_name': forms.TextInput(
                attrs={
                    'placeholder': 'Ingrese sus nombres',
                }
            ),
            'last_name': forms.TextInput(
                attrs={
                    'placeholder': 'Ingrese sus apellidos',
                }
            ),
            'email': forms.TextInput(
                attrs={
                    'placeholder': 'Ingrese su email',
                }
            ),
            'username': forms.TextInput(
                attrs={
                    'placeholder': 'Ingrese su username',
                }
            ),
            'password': forms.PasswordInput(render_value=True,
                                            attrs={
                                                'placeholder': 'Ingrese su password',
                                            }
                                            ),
            'groups': forms.SelectMultiple(attrs={
                'class': 'form-control select2',
                'style': 'width: 100%',
                'multiple': 'multiple'
            })
        }
        exclude = ['user_permissions', 'last_login',
                   'date_joined', 'is_superuser', 'is_active', 'is_staff']
        
        def clean_groups(self):
            groups = self.cleaned_data.get('groups')
            for group in groups:
                if not group.user_set.count() == 0:
                    raise forms.ValidationError("Este grupo ya está asignado a otro usuario.")
            return groups


class ProfileForm(ModelForm):

    class Meta:
    
        model = Profile
        fields = ('apellido_paterno', 'apellido_materno', 'fecha_cumple', 'direccion', 'tel', 'facebook', 'twitter', 'ciudad', 'estado', 'empresa_institucion', 'cargo', 'licenciatura', 'universidad_licenciatura', 'maestria', 'universidad_maestria', 'doctorado', 'universidad_doctorado', 'photo', 'experiencia', 'boletin')
        widgets = {
            'apellido_paterno': forms.TextInput(attrs={'class': 'form-control', 'icon_class': 'fas fa-table', 'placeholder': 'Apellido paterno', 'class': 'form-control'}),
            'apellido_materno': forms.TextInput(attrs={'class': 'form-control', 'icon_class': 'fas fa-table', 'placeholder': 'Apellido materno', 'class': 'form-control'}),
            'fecha_cumple': forms.DateInput(attrs={'class': 'form-control', 'icon_class': 'fas fa-table', 'placeholder': 'Fecha de cumpleaños ', 'class': 'form-control fecha-input'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control', 'icon_class': 'fas fa-table', 'placeholder': 'Dirección', 'class': 'form-control'}),
            'tel': forms.TextInput(attrs={'class': 'form-control', 'icon_class': 'fas fa-table', 'placeholder': 'Teléfono', 'class': 'form-control'}),
            'facebook': forms.TextInput(attrs={'class': 'form-control', 'icon_class': 'fas fa-table', 'placeholder': 'Facebook', 'class': 'form-control'}),
            'twitter': forms.TextInput(attrs={'class': 'form-control', 'icon_class': 'fas fa-table', 'placeholder': 'Twitter', 'class': 'form-control'}),
            'ciudad': forms.TextInput(attrs={'class': 'form-control', 'icon_class': 'fas fa-table', 'placeholder': 'Ciudad', 'class': 'form-control'}),
            'estado': forms.TextInput(attrs={'class': 'form-control', 'icon_class': 'fas fa-table', 'placeholder': 'Estado', 'class': 'form-control'}),
            'empresa_institucion': forms.TextInput(attrs={'class': 'form-control', 'icon_class': 'fas fa-table', 'placeholder': 'Empresa o institución', 'class': 'form-control'}),
            'cargo': forms.TextInput(attrs={'class': 'form-control', 'icon_class': 'fas fa-table', 'placeholder': 'Cargo', 'class': 'form-control'}),
            'licenciatura': forms.TextInput(attrs={'class': 'form-control', 'icon_class': 'fas fa-table', 'placeholder': 'Licenciatura', 'class': 'form-control'}),
            'universidad_licenciatura': forms.TextInput(attrs={'class': 'form-control', 'icon_class': 'fas fa-table', 'placeholder': 'Universidad de licenciatura', 'class': 'form-control'}),
            'maestria': forms.TextInput(attrs={'class': 'form-control', 'icon_class': 'fas fa-table', 'placeholder': 'Maestría', 'class': 'form-control'}),
            'universidad_maestria': forms.TextInput(attrs={'class': 'form-control', 'icon_class': 'fas fa-table', 'placeholder': 'Universidad de maestría', 'class': 'form-control'}),
            'doctorado': forms.TextInput(attrs={'class': 'form-control', 'icon_class': 'fas fa-table', 'placeholder': 'Doctorado', 'class': 'form-control'}),
            'universidad_doctorado': forms.TextInput(attrs={'class': 'form-control', 'icon_class': 'fas fa-table', 'placeholder': 'Universidad de doctorado', 'class': 'form-control'}),
            'experiencia': forms.Textarea(attrs={'class': 'form-control', 'icon_class': 'fas fa-table', 'placeholder': 'Experiencia', 'class': 'form-control'}),
            'photo': forms.ClearableFileInput(attrs={'class': 'form-control', 'icon_class': 'fas fa-table', 'placeholder': 'Imagen de perfil', 'class': 'form-control'})
            
        }
    
    

        


class CustomUserCreationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].required = False
        self.fields['password2'].required = False
        self.fields['password1'].widget = PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Contraseña', 'icon_class': 'fas fa-key'})
        self.fields['password2'].widget = PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirmar contraseña', 'icon_class': 'fas fa-key'})

    
    print("CustomUserCreationForm")

    username = forms.CharField(max_length=100, label='Nombre de Usuario', widget=forms.TextInput(
        attrs={'class': 'form-control', 'icon_class': 'fas fa-table', 'placeholder': 'Nombre de usuario', 'class': 'form-control'}))
    first_name = forms.CharField(max_length=100, label='Nombre', widget=forms.TextInput(
        attrs={'class': 'form-control', 'icon_class': 'fas fa-table', 'placeholder': 'Nombre', 'class': 'form-control'}))
    last_name = forms.CharField(max_length=100, label='Apellido Paterno', widget=forms.TextInput(
        attrs={'class': 'form-control', 'icon_class': 'fas fa-table', 'placeholder': 'Apellido paterno', 'class': 'form-control'}))
    apellido_materno = forms.CharField(max_length=100, label='Apellido Materno', widget=forms.TextInput(
        attrs={'class': 'form-control', 'icon_class': 'fas fa-table', 'placeholder': 'Apellido materno', 'class': 'form-control'}))
    fecha_cumple = forms.DateField(required=False, widget=DateInput(
        attrs={'class': 'form-control fecha-input', 'icon_class': 'fas fa-table', 'placeholder': 'Fecha de cumpleaños', 'class': 'form-control'}), label='Fecha de Cumpleaños')
    direccion = forms.CharField(max_length=100, label='Dirección', widget=forms.TextInput(
        attrs={'class': 'form-control', 'icon_class': 'fas fa-table', 'placeholder': 'Dirección', 'class': 'form-control'}))
    tel = forms.CharField(max_length=100, required=False, label='Teléfono',
                          widget=forms.TextInput(attrs={'class': 'form-control', 'icon_class': 'fas fa-table', 'placeholder': 'Teléfono', 'class': 'form-control'}))
    email = forms.EmailField(max_length=100, label='Correo Electrónico', widget=forms.EmailInput(
        attrs={'class': 'form-control', 'icon_class': 'fas fa-table', 'placeholder': 'Correo electrónico', 'class': 'form-control'}))
    facebook = forms.CharField(max_length=100, required=False, widget=forms.TextInput(
        attrs={'class': 'form-control', 'icon_class': 'fas fa-table', 'placeholder': 'Facebook', 'class': 'form-control'}))
    twitter = forms.CharField(max_length=100, required=False, widget=forms.TextInput(
        attrs={'class': 'form-control', 'icon_class': 'fas fa-table', 'placeholder': 'Twitter', 'class': 'form-control'}))
    ciudad = forms.CharField(max_length=100, required=False, widget=forms.TextInput(
        attrs={'class': 'form-control', 'icon_class': 'fas fa-table', 'placeholder': 'Ciudad', 'class': 'form-control'}))
    estado = forms.CharField(max_length=100, required=False, widget=forms.TextInput(
        attrs={'class': 'form-control', 'icon_class': 'fas fa-table', 'placeholder': 'Estado', 'class': 'form-control'}))
    empresa_institucion = forms.CharField(max_length=100, required=False, label='Empresa o Institución', widget=forms.TextInput(
        attrs={'class': 'form-control', 'icon_class': 'fas fa-table', 'placeholder': 'Empresa o institución', 'class': 'form-control'}))
    cargo = forms.CharField(max_length=100, required=False,
                            widget=forms.TextInput(attrs={'class': 'form-control', 'icon_class': 'fas fa-table', 'placeholder': 'Cargo', 'class': 'form-control'}))
    licenciatura = forms.CharField(max_length=100, required=False, widget=forms.TextInput(
        attrs={'class': 'form-control', 'icon_class': 'fas fa-table', 'placeholder': 'Licenciatura', 'class': 'form-control'}))
    universidad_licenciatura = forms.CharField(max_length=100, required=False, widget=forms.TextInput(
        attrs={'class': 'form-control', 'icon_class': 'fas fa-table', 'placeholder': 'Universidad de la licenciatura', 'class': 'form-control'}))
    maestria = forms.CharField(max_length=100, required=False, widget=forms.TextInput(
        attrs={'class': 'form-control', 'icon_class': 'fas fa-table', 'placeholder': 'Maestría', 'class': 'form-control'}))
    universidad_maestria = forms.CharField(max_length=100, required=False, widget=forms.TextInput(
        attrs={'class': 'form-control', 'icon_class': 'fas fa-table', 'placeholder': 'Universidad de la maestría', 'class': 'form-control'}))
    doctorado = forms.CharField(max_length=100, required=False, widget=forms.TextInput(
        attrs={'class': 'form-control', 'icon_class': 'fas fa-table', 'placeholder': 'Doctorado', 'class': 'form-control'}))
    universidad_doctorado = forms.CharField(max_length=100, required=False, widget=forms.TextInput(
        attrs={'class': 'form-control', 'icon_class': 'fas fa-table', 'placeholder': 'Universidad del doctorado', 'class': 'form-control'}))
    photo = forms.ImageField(widget=forms.ClearableFileInput(
        attrs={'class': 'form-control-file','multiple': True}), label='Fotografía', required=False)
    experiencia = forms.CharField(widget=forms.Textarea(
        attrs={'class': 'form-control', 'placeholder': 'Experiencia'}), required=False)
    boletin = forms.BooleanField(
        required=False, label='Deseo recibir boletín de noticias',
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))
    group = forms.ModelChoiceField(
        queryset=Group.objects.all(), label='Rol / Permisos',
        widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        widgets = {
            'fecha_cumple': DateInput(),
        }

        fields = ('username', 'first_name', 'last_name', 'apellido_materno', 'fecha_cumple', 'direccion', 'tel', 'email', 'facebook', 'twitter', 'ciudad', 'estado', 'empresa_institucion',
                  'cargo', 'licenciatura', 'universidad_licenciatura', 'maestria', 'universidad_maestria', 'doctorado', 'universidad_doctorado', 'photo', 'experiencia', 'boletin', 'group')

    def clean_imagen(self):
        imagen = self.cleaned_data.get('photo', False)
        if imagen:
            print(imagen.size)
            if imagen.size > self.MAX_SIZE_MB * 1024 * 1024:
                raise ValidationError(f"La imagen no debe superar {self.MAX_SIZE_MB} MB de tamaño.")
        return imagen
    
    def cleaned_data(self):
        cleaned_data = super().cleaned_data()
        email = cleaned_data.get('email')
        username = cleaned_data.get('username')
        if email and User.objects.filter(email=email).exists():
            print("paso 1 cleaned_data")
            self.add_error('email', 'Este correo electrónico ya está en uso.')
        if username and User.objects.filter(username=username).exists():
            print("paso 2 cleaned_data")
            self.add_error('username', 'Este nombre de usuario ya está en uso.')
        return cleaned_data
    
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


class CustomUserUpdateForm(UserChangeForm):
    

    username = forms.CharField(max_length=100, label='Nombre de Usuario', widget=forms.TextInput(
        attrs={'class': 'form-control', 'icon_class': 'fas fa-table', 'placeholder': 'Nombre de usuario', 'class': 'form-control'}))
    first_name = forms.CharField(max_length=100, label='Nombre', widget=forms.TextInput(
        attrs={'class': 'form-control', 'icon_class': 'fas fa-table', 'placeholder': 'Nombre', 'class': 'form-control'}))
    last_name = forms.CharField(max_length=100, label='Apellido Paterno', widget=forms.TextInput(
        attrs={'class': 'form-control', 'icon_class': 'fas fa-table', 'placeholder': 'Apellido paterno', 'class': 'form-control'}))
    apellido_materno = forms.CharField(max_length=100, label='Apellido Materno', widget=forms.TextInput(
        attrs={'class': 'form-control', 'icon_class': 'fas fa-table', 'placeholder': 'Apellido materno', 'class': 'form-control'}))
    fecha_cumple = forms.DateField(required=False, widget=DateInput(
        attrs={'class': 'form-control fecha-input', 'icon_class': 'fas fa-table', 'placeholder': 'Fecha de cumpleaños', 'class': 'form-control'}), label='Fecha de Cumpleaños')
    direccion = forms.CharField(max_length=100, label='Dirección', widget=forms.TextInput(
        attrs={'class': 'form-control', 'icon_class': 'fas fa-table', 'placeholder': 'Dirección', 'class': 'form-control'}))
    tel = forms.CharField(max_length=100, required=False, label='Teléfono',
                          widget=forms.TextInput(attrs={'class': 'form-control', 'icon_class': 'fas fa-table', 'placeholder': 'Teléfono', 'class': 'form-control'}),
                          validators=[RegexValidator(r'^\d{10}$', 'Ingresa un número de teléfono válido.')])
    email = forms.EmailField(max_length=100, label='Correo Electrónico', widget=forms.EmailInput(
        attrs={'class': 'form-control', 'icon_class': 'fas fa-table', 'placeholder': 'Correo electrónico', 'class': 'form-control'}))
    facebook = forms.CharField(max_length=100, required=False, widget=forms.TextInput(
        attrs={'class': 'form-control', 'icon_class': 'fas fa-table', 'placeholder': 'Facebook', 'class': 'form-control'}))
    twitter = forms.CharField(max_length=100, required=False, widget=forms.TextInput(
        attrs={'class': 'form-control', 'icon_class': 'fas fa-table', 'placeholder': 'Twitter', 'class': 'form-control'}))
    ciudad = forms.CharField(max_length=100, required=False, widget=forms.TextInput(
        attrs={'class': 'form-control', 'icon_class': 'fas fa-table', 'placeholder': 'Ciudad', 'class': 'form-control'}))
    estado = forms.CharField(max_length=100, required=False, widget=forms.TextInput(
        attrs={'class': 'form-control', 'icon_class': 'fas fa-table', 'placeholder': 'Estado', 'class': 'form-control'}))
    empresa_institucion = forms.CharField(max_length=100, required=False, label='Empresa o Institución', widget=forms.TextInput(
        attrs={'class': 'form-control', 'icon_class': 'fas fa-table', 'placeholder': 'Empresa o institución', 'class': 'form-control'}))
    cargo = forms.CharField(max_length=100, required=False, label='Cargo',
                            widget=forms.TextInput(attrs={'class': 'form-control', 'icon_class': 'fas fa-table', 'placeholder': 'Cargo', 'class': 'form-control'}))
    licenciatura = forms.CharField(max_length=100, required=False, widget=forms.TextInput(
        attrs={'class': 'form-control', 'icon_class': 'fas fa-table', 'placeholder': 'Licenciatura', 'class': 'form-control'}))
    universidad_licenciatura = forms.CharField(max_length=100, required=False, widget=forms.TextInput(
        attrs={'class': 'form-control', 'icon_class': 'fas fa-table', 'placeholder': 'Universidad de la licenciatura', 'class': 'form-control'}))
    maestria = forms.CharField(max_length=100, required=False, widget=forms.TextInput(
        attrs={'class': 'form-control', 'icon_class': 'fas fa-table', 'placeholder': 'Maestría', 'class': 'form-control'}))
    universidad_maestria = forms.CharField(max_length=100, required=False, widget=forms.TextInput(
        attrs={'class': 'form-control', 'icon_class': 'fas fa-table', 'placeholder': 'Universidad de la maestría', 'class': 'form-control'}))
    doctorado = forms.CharField(max_length=100, required=False, widget=forms.TextInput(
        attrs={'class': 'form-control', 'icon_class': 'fas fa-table', 'placeholder': 'Doctorado', 'class': 'form-control'}))
    universidad_doctorado = forms.CharField(max_length=100, required=False, widget=forms.TextInput(
        attrs={'class': 'form-control', 'icon_class': 'fas fa-table', 'placeholder': 'Universidad del doctorado', 'class': 'form-control'}))
    photo = forms.ImageField(widget=forms.ClearableFileInput(
        attrs={'class': 'form-control-file','multiple': True}), label='Fotografía', required=False)
    experiencia = forms.CharField(widget=forms.Textarea(
        attrs={'class': 'form-control', 'placeholder': 'Experiencia'}), required=False)
    boletin = forms.BooleanField(
        required=False, label='Deseo recibir boletín de noticias',
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))
    group = forms.ModelChoiceField(
        queryset=Group.objects.all(), label='Rol / Permisos',
        widget=forms.Select(attrs={'class': 'form-control'}))
    new_password = forms.CharField(max_length=100, required=False, widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Nueva contraseña', 'icon_class': 'fas fa-key'}), label='Nueva Contraseña')
    confirm_password = forms.CharField(max_length=100, required=False, widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Confirmar contraseña', 'icon_class': 'fas fa-key'}), label='Confirmar Contraseña')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:  # Verifica si el objeto tiene una clave primaria (es una instancia existente)
            self.fields['group'].initial = self.instance.groups.first()
            self.fields['group'].widget.attrs['class'] = 'form-control'  # Aplica la clase form-control de Bootstrap al campo)
    
    def clean_facebook(self):
        facebook = self.cleaned_data.get('facebook')
        if facebook:
            url_validator = URLValidator()
            try:
                url_validator(facebook)
            except ValidationError:
                raise forms.ValidationError('Ingresa una URL válida para Facebook.')
        return facebook

    def clean_twitter(self):
        twitter = self.cleaned_data.get('twitter')
        if twitter:
            url_validator = URLValidator()
            try:
                url_validator(twitter)
            except ValidationError:
                raise forms.ValidationError('Ingresa una URL válida para Twitter.')
        return twitter

    class Meta:
        model = User
        widgets = {
            'fecha_cumple': DateInput(),
        }

        fields = ('username', 'first_name', 'last_name', 'apellido_materno', 'fecha_cumple', 'direccion', 'tel', 'email', 'facebook', 'twitter', 'ciudad', 'estado', 'empresa_institucion',
                  'cargo', 'licenciatura', 'universidad_licenciatura', 'maestria', 'universidad_maestria', 'doctorado', 'universidad_doctorado', 'photo', 'experiencia', 'boletin', 'group')

    def clean_imagen(self):
        imagen = self.cleaned_data.get('photo', False)
        if imagen:
            print(imagen.size)
            if imagen.size > self.MAX_SIZE_MB * 1024 * 1024:
                raise ValidationError(f"La imagen no debe superar {self.MAX_SIZE_MB} MB de tamaño.")
        return imagen
    
    def cleaned_data(self):
        print("cleaned_data")
        cleaned_data = super().cleaned_data()
        email = cleaned_data.get('email')
        username = cleaned_data.get('username')
        if email and User.objects.filter(email=email).exists():
            print("paso 1 cleaned_data")
            self.add_error('email', 'Este correo electrónico ya está en uso.')
        if username and User.objects.filter(username=username).exists():
            print("paso 2 cleaned_data")
            self.add_error('username', 'Este nombre de usuario ya está en uso.')
        return cleaned_data
    
    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get('new_password')
        confirm_password = cleaned_data.get('confirm_password')
        if new_password and confirm_password and new_password != confirm_password:
            self.add_error('confirm_password', 'Las contraseñas no coinciden.')
        return cleaned_data
    
    def save(self, commit=True):

        user = super().save(commit=False)

        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']

        new_password = self.cleaned_data['new_password']
        if new_password:
            user.set_password(new_password)  # Actualizar la contraseña si se proporciona una nueva

        if 'photo' in self.changed_data:
            photo = self.cleaned_data['photo']
            if photo:
                user.profile.photo = photo  # Asignar directamente el archivo al campo 'photo' del perfil

        

        # update fecha_cumple and direccion in Profile
        try:
            profile = Profile.objects.get(user=user)
        except Profile.DoesNotExist:
            profile = Profile(user=user)

        profile.apellido_materno = self.cleaned_data['apellido_materno']
        profile.apellido_paterno = self.cleaned_data['last_name']
        profile.direccion = self.cleaned_data['direccion']
        profile.fecha_cumple = self.cleaned_data['fecha_cumple']
        profile.tel = self.cleaned_data['tel']
        profile.facebook = self.cleaned_data['facebook']
        profile.twitter = self.cleaned_data['twitter']
        profile.ciudad = self.cleaned_data['ciudad']
        profile.estado = self.cleaned_data['estado']
        profile.empresa_institucion = self.cleaned_data['empresa_institucion']
        profile.cargo = self.cleaned_data['cargo']
        profile.licenciatura = self.cleaned_data['licenciatura']
        profile.universidad_licenciatura = self.cleaned_data['universidad_licenciatura']
        profile.maestria = self.cleaned_data['maestria']
        profile.universidad_maestria = self.cleaned_data['universidad_maestria']
        profile.doctorado = self.cleaned_data['doctorado']
        profile.universidad_doctorado = self.cleaned_data['universidad_doctorado']
        # profile.photo = self.cleaned_data['photo']
        profile.experiencia = self.cleaned_data['experiencia']
        profile.boletin = self.cleaned_data['boletin']
        profile.save()

        if commit:
            user.save()
            self.cleaned_data['group'].user_set.add(user)

        return user
