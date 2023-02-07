from django.contrib import admin

# Register your models here.
from .models import Categorias
from .models import SeccionesCentroDocumental

admin.site.register(Categorias)
admin.site.register(SeccionesCentroDocumental)