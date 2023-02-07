from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Profile
from django.contrib.auth.models import User
from django.db import models


class DateInput(forms.DateInput):
    input_type = 'date'


class CustomUserCreationForm(UserCreationForm):

    username = forms.CharField(max_length=100, label='Nombre de Usuario')
    first_name = forms.CharField(max_length=100, label='Nombre')
    last_name = forms.CharField(max_length=100, label='Apellido Paterno')
    apellido_materno = forms.CharField(max_length=100, label='Apellido Materno')
    fecha_cumple = forms.DateField(required=False, widget=DateInput, label='Fecha de Cumpleaños')
    direccion = forms.CharField(max_length=100, label='Dirección')
    tel = forms.CharField(max_length=100, required=False ,label='Teléfono')
    email = forms.EmailField(max_length=100, label='Correo Electrónico')
    facebook = forms.CharField(max_length=100, required=False)
    twitter = forms.CharField(max_length=100, required=False)
    ciudad = forms.CharField(max_length=100, required=False)
    estado = forms.CharField(max_length=100, required=False)
    empresa_institucion = forms.CharField(max_length=100, required=False,label='Empresa o Institución')
    cargo = forms.CharField(max_length=100, required=False)
    licenciatura = forms.CharField(max_length=100, required=False)
    universidad_licenciatura = forms.CharField(max_length=100, required=False)
    maestria = forms.CharField(max_length=100, required=False)
    universidad_maestria = forms.CharField(max_length=100, required=False)
    doctorado = forms.CharField(max_length=100, required=False)
    universidad_doctorado = forms.CharField(max_length=100, required=False)
    photo = forms.ImageField(widget=forms.ClearableFileInput(attrs={'multiple': True}) , label='Fotografía')
    experiencia = forms.CharField(widget=forms.Textarea, required=False)
    boletin = forms.BooleanField(required=False ,label='Deseo recibir boletín de noticias')

    class Meta:
        model = User
        widgets = {
            'fecha_cumple': DateInput(),
        }
        fields = ('username', 'first_name', 'last_name', 'apellido_materno', 'fecha_cumple', 'direccion', 'tel', 'email', 'facebook', 'twitter', 'ciudad', 'estado', 'empresa_institucion',
                  'cargo', 'licenciatura', 'universidad_licenciatura', 'maestria', 'universidad_maestria', 'doctorado', 'universidad_doctorado', 'photo', 'experiencia', 'boletin')

    def save(self, commit=True):

        user = super().save(commit=False)

        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']

        if commit:
            user.save()

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