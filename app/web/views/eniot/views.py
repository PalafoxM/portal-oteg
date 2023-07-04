from django.views.generic import TemplateView
from back.models import Eniot, EniotAlbun
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
import requests
from django.shortcuts import redirect
from django.http import StreamingHttpResponse
from django.views.generic import TemplateView, View
from web.models import *

class EniotView(TemplateView):
    template_name = 'web/paginas/eniot/eniot.html'
    try:
        encuesta = Encuesta.objects.filter(seccion=2, activo=True).latest('fecha_registro')
        print(encuesta.seccion)
        print(encuesta.url)
    except Encuesta.DoesNotExist:
        print("No matching Encuesta found.")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pdf =  Eniot.objects.filter(seccion='programa-eniot').order_by('-date_created')[:1].get()
        context['pdf'] = pdf
        context['nav_title'] = 'ENIOT'
        context['img_url'] = 'img_nav/preguntas.png'
        context['encuesta'] = self.encuesta 
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
        context['tipo'] =  'eniot_pdf_viewer'
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
        
        context['tipo'] =  'eniot_ponencia_eventos_pdf_viewer'
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
        context['img_url'] = 'img_nav/pdf.png'

        print(fotos)
        print(albums)
        return context

class MemoriasPDFViewer (TemplateView):
    template_name = 'web/paginas/eniot/pdf_viewer.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pdf = get_object_or_404(Eniot, id=self.kwargs.get('pk'))
        context['pdf'] = pdf
        context['nav_title'] = pdf.nombrePDF
        context['img_url'] = 'img_nav/pdf.png'
        context['list'] =  reverse_lazy('eniot_memorias')
        return context

class PonenciaEventosPDFViewer (TemplateView):
    template_name = 'web/paginas/eniot/pdf_viewer.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pdf = get_object_or_404(Eniot, id=self.kwargs.get('pk'))
        context['pdf'] = pdf
        context['nav_title'] = pdf.nombrePDF
        context['img_url'] = 'img_nav/pdf.png'
        context['list'] =  reverse_lazy('eniot_ponencia_eventos')
        return context
    
class PDFDownloadEniot(View):
    def get(self, request, *args, **kwargs):
        # Get the PDF object
        pdf = get_object_or_404(Eniot, id=kwargs['pk'])

        # Construct the complete URL
        # complete_url = 'https://portal-oteg.s3.amazonaws.com/media/' + pdf.doc_url

        # Download the file from the URL
        r = requests.get(pdf.doc_url.url, stream=True)
        # how to know the request is successful?
        if r.status_code != 200:
            return redirect('eniot')

        # Send the file as a response
        response = StreamingHttpResponse(r.iter_content(chunk_size=1024))
        response['Content-Type'] = 'application/pdf'
        response['Content-Disposition'] = 'attachment; filename="%s.pdf"' % pdf.nombrePDF

        try:
            pdf.num_descargas += 1
            pdf.save()
        except (ConnectionResetError, BrokenPipeError):
            pass
        return response