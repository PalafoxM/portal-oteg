from django.forms import ModelForm, TextInput
from contenido.models import *

class BannerForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # for form in self.visible_fields():
        #     form.field.widget.attrs['class'] = 'form-control'


    class Meta:
        model = Banner
        fields = '__all__'
        widgets = {
            'name': TextInput(attrs = { 'placeholder': 'Ingresa una Nombre'}),
            'banner_url': TextInput(attrs = { 'placeholder': 'Ingresa un Enlace'}), 
        }
    
    # def save(self, commit=True):
    #     data = {}
    #     form = super()
    #     try:
    #         if form.is_valid():
    #             form.save()
    #         else:
    #             data['error'] = form.errors
    #     except Exception as e:
    #         data['error'] = str(e)
    #     return data
    
class PlacesOfInterestForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


    class Meta:
        model = PlacesOfInterest
        fields = '__all__'
        widgets = {
            'sito_web': TextInput(attrs = { 'placeholder': 'Ingresa un Sitio Web'}),
            'decription': TextInput(attrs = { 'placeholder': 'Ingresa un Descripcion'}), 
        }
    
    # def save(self, commit=True):
    #     data = {}
    #     form = super()
    #     try:
    #         if form.is_valid():
    #             form.save()
    #         else:
    #             data['error'] = form.errors
    #     except Exception as e:
    #         data['error'] = str(e)
    #     return data
