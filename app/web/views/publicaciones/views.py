from django.views.generic import TemplateView , View 
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from web.models import PerfilVisistantePDF , BarometroTuristico
from django.http import HttpResponse ,StreamingHttpResponse
from django.core.signals import request_finished
from django.dispatch import receiver
from itertools import groupby
from operator import attrgetter
from django.db.models import F
import requests
from django.http import JsonResponse
from django.views.decorators.http import require_GET

#Perfil de Visitante a Ciudad

class PerfilVisitanteCiudad (TemplateView):

    template_name = 'web/paginas/publicaciones/perfil_visitante_ciudad.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Perfil de visitante'
        pdfs = PerfilVisistantePDF.objects.filter(seccion=self.kwargs.get('pk')).order_by('subseccion', '-yearPDF')
        grouped_pdfs = groupby(pdfs, attrgetter('subseccion'))

        subseccion_data = []
        for subseccion, subseccion_pdfs in grouped_pdfs:
            subseccion_data.append((subseccion, list(subseccion_pdfs)))
        context['current_seccion'] = self.kwargs.get('pk')
        context['subseccion_data'] = subseccion_data
        return context
    

    
class PublicacionesPDFViewer (TemplateView):
    template_name = 'web/paginas/publicaciones/pdf_viewer.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pdf = get_object_or_404(PerfilVisistantePDF, id=self.kwargs.get('pk'))
        context['pdf'] = pdf
        return context
    

class PDFDownloadView(View):
    def get(self, request, *args, **kwargs):
        # Get the PDF object
        pdf = get_object_or_404(PerfilVisistantePDF, id=kwargs['pk'])

        # Download the file from the URL
        r = requests.get(pdf.url, stream=True)
        # how to know the request is successful?
        if r.status_code != 200:
            return redirect('perfil_visistante_ciudad')
        
        # Send the file as a response
        response = StreamingHttpResponse(r.iter_content(chunk_size=1024))
        response['Content-Type'] = 'application/pdf'
        response['Content-Disposition'] = 'attachment; filename="%s.pdf"' % pdf.nombrePDF

        try:
            pdf.num_descargas += 1
            pdf.save()
        except (ConnectionResetError ,BrokenPipeError):
            pass
        return response
    
# Perfil de Visitante a Evento
class PotenciasEventos (TemplateView):
    template_name = 'web/paginas/publicaciones/ponencias_eventos.html'

class RevistaOTEG (TemplateView):
    template_name = 'web/paginas/publicaciones/revista_oteg.html'

class OtasPublicaciones (TemplateView):
    template_name = 'web/paginas/publicaciones/otras_publicaciones.html'

class InventarioTuristico (TemplateView):
    template_name = 'web/paginas/publicaciones/inventario_turistico.html'

class PDFDownloadBarometro(View):
    def get(self, request, *args, **kwargs):
        # Get the PDF object
        pdf = get_object_or_404(BarometroTuristico, id=kwargs['pk'])

        # Download the file from the URL
        r = requests.get(pdf.url, stream=True)
        # how to know the request is successful?
        if r.status_code != 200:
            return redirect('perfil_visistante_ciudad')
        
        # Send the file as a response
        response = StreamingHttpResponse(r.iter_content(chunk_size=1024))
        response['Content-Type'] = 'application/pdf'
        response['Content-Disposition'] = 'attachment; filename="%s.pdf"' % pdf.nombrePDF

        try:
            pdf.num_descargas += 1
            pdf.save()
        except (ConnectionResetError ,BrokenPipeError):
            pass
        return response

class BarometroTuristicoView(TemplateView):

    template_name = 'web/paginas/publicaciones/barometro_turistico.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pdf =  most_recent_register = BarometroTuristico.objects.latest('fecha_registro')

        distinct_years = BarometroTuristico.objects.values('yearPDF').distinct().order_by('yearPDF')
        years_list = [item['yearPDF'] for item in distinct_years]
        context['years'] = years_list
        context['pdf'] = pdf
        return context


# Noticias Turisticas
class NoticiasTuristicasView(TemplateView):
        template_name = 'web/paginas/publicaciones/noticias_turisticas.html'
    
        def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            context['title'] = 'Noticias Turisticas'
            return context


@require_GET
def search(request):
    q = request.GET.get('q', '')
    year = request.GET.get('year', '')
    bim = request.GET.get('bim', '')

    results = BarometroTuristico.objects.filter(nombrePDF__icontains=q)
    if year:
        results = results.filter(yearPDF__icontains=year)
    if bim:
        results = results.filter(semestre__icontains=bim)

    data = [{'nombrePDF': obj.nombrePDF, 'url': obj.url} for obj in results]
    return JsonResponse(data, safe=False)

