from django.views.generic import TemplateView
from web.models import BarometroTuristico 
from back.models import Eniot, EniotAlbun
from collections import defaultdict


class EniotView(TemplateView):
    template_name = 'web/paginas/eniot/eniot.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pdf =  Eniot.objects.filter(seccion='programa-eniot').order_by('-date_created')[:1].get()
        context['pdf'] = pdf
        context['nav_title'] = 'ENIOT'
        return context
    
class ProgramaProximaEdicion(TemplateView):
    template_name = 'web/paginas/eniot/eniot.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pdf = Eniot.objects.filter(seccion='programa-eniot').order_by('-date_created')[:1].get()
        context['pdf'] = pdf
        context['nav_title'] = 'Programa ENIOT'
        return context
    
class MemoriasView(TemplateView):
    template_name = 'web/paginas/eniot/memorias.html'

    def get_queryset(self):
        # Filtrar los PDF por la sección 'memorias'
        queryset = Eniot.objects.filter(seccion='memorias').order_by('-date_created')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Obtener los años únicos de los PDF
        years = Eniot.objects.filter(seccion='memorias').order_by('anio').values_list('anio', flat=True).distinct()

        # Crear un diccionario para almacenar los PDF clasificados por año
        pdf_by_year = {}

        # Clasificar los PDF por año
        for year in years:
            pdf_by_year[year] = Eniot.objects.filter(seccion='memorias', anio=year).order_by('-date_created')

        context['pdf_by_year'] = pdf_by_year
        context['nav_title'] = 'Memorias'
        return context

class PonenciaEventosView(TemplateView):
    template_name = 'web/paginas/eniot/memorias.html'

    def get_queryset(self):
        # Filtrar los PDF por la sección 'ponencia-eventos'
        queryset = Eniot.objects.filter(seccion='ponencia-eventos').order_by('-date_created')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Obtener los años únicos de los PDF
        years = Eniot.objects.filter(seccion='ponencia-eventos').order_by('anio').values_list('anio', flat=True).distinct()

        # Crear un diccionario para almacenar los PDF clasificados por año
        pdf_by_year = {}

        # Clasificar los PDF por año
        for year in years:
            pdf_by_year[year] = Eniot.objects.filter(seccion='ponencia-eventos', anio=year).order_by('-date_created')

        context['pdf_by_year'] = pdf_by_year
        context['nav_title'] = 'Ponencia a Eventos'
        return context
    
class EniotEventosFotosView(TemplateView):
    template_name = 'web/paginas/eniot/eniot-fotos.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Obtener solo los valores únicos de nombreAlbun
        albums = EniotAlbun.objects.order_by('nombreAlbun').values_list('nombreAlbun', flat=True).distinct()

        # Obtener las fotos por álbum
        fotos_por_album = {}
        fotos = EniotAlbun.objects.filter()

        context['albums'] = albums
        context['fotos'] = fotos
        context['nav_title'] = 'Ultimos Eventos'

        print(fotos)
        print(albums)
        return context