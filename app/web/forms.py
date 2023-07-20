from django import forms
import re
import pycountry

EMAIL_REGEX = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"

class SenEmail(forms.Form):
    
    COUNTRIES = [(country.name, country.name) for country in pycountry.countries]
    COUNTRIES.insert(0, ('', 'Selecciona un País'))

    email = forms.EmailField( widget=forms.TextInput(attrs = { 'placeholder': 'Ingresa un correo', 'class':'col-md-6'}), required=True, label="Correo electrónico")
    country = forms.ChoiceField(
        choices=COUNTRIES,
        widget=forms.Select(attrs={'placeholder': 'Seleccione el país', 'class': 'col-md-6'}),
        required=True,
        label="País"
    )
    subject = forms.CharField(widget=forms.TextInput(attrs = { 'placeholder': 'Agrega tu nombre'}), max_length=100, required=True, label="Nombre completo")
    message = forms.CharField(widget=forms.Textarea(attrs = { 'placeholder': 'Agrega el mensaje'}), required=True, label="Requerimiento y objetivo de la solicitud*")

    def clean_email(self):
        email = self.cleaned_data.get('email')

        if email and not re.match(EMAIL_REGEX, email):
            raise forms.ValidationError('Invalid email format')

        return email