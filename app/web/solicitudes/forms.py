from django import forms
import re

EMAIL_REGEX = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"

class SenEmail(forms.Form):
    email = forms.EmailField( widget=forms.TextInput(attrs = { 'placeholder': 'Ingresa un correo'}), required=True, label="Correo Electronico")
    subject = forms.CharField(widget=forms.TextInput(attrs = { 'placeholder': 'Agrega tu nombre'}), max_length=100, required=True, label="Nombre completo")
    message = forms.CharField(widget=forms.Textarea(attrs = { 'placeholder': 'Agrega el mensaje'}), required=True, label="Mensaje")
    contry = forms.CharField(widget=forms.TextInput(attrs = { 'placeholder': 'Ingresa el pais'}), required=True, label="Pais")

    def clean_email(self):
        email = self.cleaned_data.get('email')

        if email and not re.match(EMAIL_REGEX, email):
            raise forms.ValidationError('Invalid email format')

        return email