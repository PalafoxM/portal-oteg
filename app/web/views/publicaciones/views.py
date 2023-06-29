from django.views.generic import TemplateView, View
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from web.models import PerfilVisistantePDF, BarometroTuristico, DataPoint, Encuesta
from back.models import *
from django.http import HttpResponse, StreamingHttpResponse
from django.core.signals import request_finished
from django.dispatch import receiver
from itertools import groupby
from operator import attrgetter
from django.db.models import F
import requests
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from back.models import Banner, Noticia
from datetime import datetime, timedelta
from django.http import Http404


# Perfil de Visitante a Ciudad
class PerfilVisitanteCiudad (TemplateView):

    template_name = 'web/paginas/publicaciones/perfil_visitante_ciudad.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Perfil de visitante'

        pdfs = PerfilVisistantePDF.objects.filter(
            seccion=self.kwargs.get('pk')).order_by('subseccion', '-yearPDF')
        grouped_pdfs = groupby(pdfs, attrgetter('subseccion'))

        subseccion_data = []
        for subseccion, subseccion_pdfs in grouped_pdfs:
            subseccion_data.append((subseccion, list(subseccion_pdfs)))
        context['current_seccion'] = self.kwargs.get('pk')
        context['subseccion_data'] = subseccion_data
        return context


class PublicacionesSecciones (TemplateView):
    template_name = 'web/paginas/publicaciones/publicaciones_secciones.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        try:
            seccion = get_object_or_404(
                SeccionesCentroDocumental, id=self.kwargs.get('pk'))
        except:
            raise Http404("No existe la seccion")

        publicaciones = Publications.objects.filter(
            section=seccion, visible=True).order_by('category', '-date_created')

        groped_publicaciones = groupby(publicaciones, attrgetter('category'))

        publicaciones_data = []
        for category, category_publicaciones in groped_publicaciones:
            publicaciones_data.append((category, list(category_publicaciones)))

        context['publicaciones_data'] = publicaciones_data

        context['seccion'] = seccion
        return context


class PublicacionesPDFViewer (TemplateView):
    template_name = 'web/paginas/publicaciones/pdf_viewer.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pdf = get_object_or_404(Publications, id=self.kwargs.get('pk'))
        context['pdf'] = pdf
        context['nav_title'] = pdf.name
        context['img_url'] = 'img_nav/pdf.png'
        return context


class PDFDownloadView(View):
    def get(self, request, *args, **kwargs):
        # Get the PDF object
        pdf = get_object_or_404(Publications, id=kwargs['pk'])

        # Download the file from the URL
        r = requests.get(pdf.doc.url, stream=True)
        # how to know the request is successful?
        if r.status_code != 200:
            return redirect('publicaciones_secciones')

        # Send the file as a response
        response = StreamingHttpResponse(r.iter_content(chunk_size=1024))
        response['Content-Type'] = 'application/pdf'
        response['Content-Disposition'] = 'attachment; filename="%s.pdf"' % pdf.name

        try:
            pdf.num_descargas += 1
            pdf.save()
        except (ConnectionResetError, BrokenPipeError):
            pass
        return response


class PDFDownloadViewBack(View):
    def get(self, request, *args, **kwargs):
        # Get the PDF object
        pdf = get_object_or_404(Publications, id=kwargs['pk'])

        # Download the file from the URL
        r = requests.get(pdf.doc.url, stream=True)
        # how to know the request is successful?
        if r.status_code != 200:
            return redirect('publicaciones_secciones')

        # Send the file as a response
        response = StreamingHttpResponse(r.iter_content(chunk_size=1024))
        response['Content-Type'] = 'application/pdf'
        response['Content-Disposition'] = 'attachment; filename="%s.pdf"' % pdf.name

        return response


class AudioDownload(View):
    def get(self, request, *args, **kwargs):
        # Get the PDF object
        pdf = get_object_or_404(Publications, id=kwargs['pk'])

        # Download the file from the URL
        r = requests.get(pdf.doc.url, stream=True)
        # how to know the request is successful?
        if r.status_code != 200:
            return redirect('publicaciones_secciones')

        # Send the file as a response
        response = StreamingHttpResponse(r.iter_content(chunk_size=1024))
        response['Content-Type'] = 'application/pdf'
        response['Content-Disposition'] = 'attachment; filename="%s.mp3"' % pdf.name

        try:
            pdf.num_descargas += 1
            pdf.save()
        except (ConnectionResetError, BrokenPipeError):
            pass
        return response


class ExelDownload(View):
    def get(self, request, *args, **kwargs):
        # Get the PDF object
        pdf = get_object_or_404(Publications, id=kwargs['pk'])

        # Download the file from the URL
        r = requests.get(pdf.doc.url, stream=True)
        # how to know the request is successful?
        if r.status_code != 200:
            return redirect('publicaciones_secciones')

        # Send the file as a response
        response = StreamingHttpResponse(r.iter_content(chunk_size=1024))
        response['Content-Type'] = 'application/pdf'
        response['Content-Disposition'] = 'attachment; filename="%s.xlsx"' % pdf.name

        try:
            pdf.num_descargas += 1
            pdf.save()
        except (ConnectionResetError, BrokenPipeError):
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
        r = requests.get(pdf.doc.url, stream=True)
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
        except (ConnectionResetError, BrokenPipeError):
            pass
        return response


class BarometroTuristicoView(TemplateView):

    template_name = 'web/paginas/publicaciones/barometro_turistico.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pdf = BarometroTuristico.objects.latest('fecha_registro')
        distinct_years = BarometroTuristico.objects.values(
            'yearPDF').distinct().order_by('yearPDF')
        years_list = [item['yearPDF'] for item in distinct_years]

        try:
            encuesta = Encuesta.objects.filter(activo=True  , seccion = 1 ).latest('fecha_registro')
        except Encuesta.DoesNotExist:
            encuesta = None
            print("No hay registros disponibles.")

        context['encuesta'] = encuesta
        context['years'] = years_list
        context['pdf'] = pdf

        context['img_url'] = 'img_nav/barometro.jpg'
        context['nav_title'] = 'BARÓMETRO TURÍSTICO'
        return context


# Noticias Turisticas
class NoticiasTuristicasView(TemplateView):
    model = Noticia
    template_name = 'web/paginas/publicaciones/noticias_turisticas.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Noticias Turisticas'
        context['publicaciones'] = Noticia.objects.order_by(
            F('fecha_nota').desc(nulls_last=True))[:10]  # order by date
        
        context['img_url'] = 'img_nav/noticia_t.png'
        context['nav_title'] = 'NOTICIAS TURÍSTICAS'
        context['noticias'] = Noticia.objects.order_by('-fecha_nota')[:10]
        return context


class ReportesMensualesView (TemplateView):
    template_name = 'web/paginas/publicaciones/reportes_mensuales.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        distinct_years = DataPoint.objects.values(
            'year').distinct().order_by('year')
        years_list = [item['year'] for item in distinct_years]
        context['years'] = years_list

        return context


class NoticiaViewer (TemplateView):
    template_name = 'web/components/noticia_viewer/noticia_viewer.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        noticia = get_object_or_404(Noticia, id=self.kwargs.get('pk'))
        context['noticia'] = noticia
        return context


class BarometroViewer (TemplateView):
    template_name = 'web/paginas/publicaciones/barometro_turistico_viewer.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        barometro = get_object_or_404(
            BarometroTuristico, id=self.kwargs.get('pk'))
        context['pdf'] = barometro
        context['img_url'] = 'img_nav/barometro.jpg'
        context['nav_title'] = 'BARÓMETRO TURÍSTICO'
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

    data = [{'nombrePDF': obj.nombrePDF, 'url': obj.doc.url, 'id': obj.id}
            for obj in results]
    return JsonResponse(data, safe=False)


@require_GET
def search_noticias(request):
    q = request.GET.get('q', '')
    year = request.GET.get('year', '')

    results = Noticia.objects.filter(titulo__icontains=q).order_by(
        F('fecha_nota').desc(nulls_last=True))

    if year:
        results = results.filter(fecha_nota__icontains=year)

    data = [{'titulo': obj.titulo, 'id': obj.id, 'fecha_nota': datetime.strftime(
        obj.fecha_nota, "%Y-%m-%d")} for obj in results]
    return JsonResponse(data, safe=False)


@require_GET
def search_words(request):
    w = request.GET.get('w', '')
    word = request.GET.get('word', '')

    if w == '':
        results = Glosario.objects.filter(palabra__icontains=word)
    else:
        results = Glosario.objects.filter(palabra__istartswith=w)

    data = [{'palabra': obj.palabra, 'definicion': obj.definicion}
            for obj in results]
    return JsonResponse(data, safe=False)


@require_GET
def chart_data(request):
    # Retrieve the filter options from the Ajax request
    filter_option = request.GET.get('filter_option', None)
    filter_option2 = request.GET.get('filter_option2', None)

    # Retrieve the data from the database based on the filter option
    queryset = DataPoint.objects.filter(
        estado=filter_option, year=filter_option2)

    # Convert the data to a format that can be used by Chart.js
    # extract the values for each month
    jan_data = [
        data.enero_data for data in queryset if data.enero_data is not None]
    feb_data = [
        data.febrero_data for data in queryset if data.febrero_data is not None]
    mar_data = [
        data.marzo_data for data in queryset if data.marzo_data is not None]
    apr_data = [
        data.abril_data for data in queryset if data.abril_data is not None]
    may_data = [
        data.mayo_data for data in queryset if data.mayo_data is not None]
    jun_data = [
        data.junio_data for data in queryset if data.junio_data is not None]
    jul_data = [
        data.julio_data for data in queryset if data.julio_data is not None]
    aug_data = [
        data.agosto_data for data in queryset if data.agosto_data is not None]
    sep_data = [
        data.septiembre_data for data in queryset if data.septiembre_data is not None]
    oct_data = [
        data.octubre_data for data in queryset if data.octubre_data is not None]
    nov_data = [
        data.noviembre_data for data in queryset if data.noviembre_data is not None]
    dec_data = [
        data.diciembre_data for data in queryset if data.diciembre_data is not None]

# combine the data into a single list
    output_list = jan_data + feb_data + mar_data + apr_data + may_data + \
        jun_data + jul_data + aug_data + sep_data + oct_data + nov_data + dec_data

    chart_data = {
        'labels': ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'],
        'values': output_list,
    }

    # Return the data in JSON format
    return JsonResponse(chart_data)
