from django.contrib import admin
# Register your models here.
from .models import * 
from .forms import *

admin.site.register(Evento)
admin.site.register(Noticia)
admin.site.register(Banner)
admin.site.register(Alba)
admin.site.register(Glosario)
admin.site.register(SeccionesCentroDocumental)
admin.site.register(Categorias)
admin.site.register(Report_Section)
admin.site.register(Publications)
admin.site.register(Categorias_Eniot)
admin.site.register(InventarioTuristico)


class repotsAdmin (admin.ModelAdmin):
    form = ReportsForm

admin.site.register(Report, repotsAdmin)
