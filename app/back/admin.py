from django.contrib import admin
# Register your models here.
from .models import * 

admin.site.register(Evento)
admin.site.register(Noticia)
admin.site.register(Banner)
admin.site.register(Alba)
admin.site.register(Glosario)
admin.site.register(SeccionesCentroDocumental)
admin.site.register(Categorias)
admin.site.register(Publications)
admin.site.register(catalogo_categorias)
admin.site.register(catalogo_destinos)