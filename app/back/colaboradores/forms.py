from django.forms import ModelForm, TextInput
from colaboradores.models import Publications

class PublicationForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # for form in self.visible_fields():
        #     form.field.widget.attrs['class'] = 'form-control'


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
