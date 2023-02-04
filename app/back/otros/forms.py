from django import forms
from .models import SeccionesCentroDocumental, Categorias


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
