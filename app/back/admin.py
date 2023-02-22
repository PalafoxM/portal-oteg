from django.contrib import admin
# Register your models here.
from .models import * 

admin.site.register(Evento)
admin.site.register(Noticia)
admin.site.register(Banner)
admin.site.register(Alba)