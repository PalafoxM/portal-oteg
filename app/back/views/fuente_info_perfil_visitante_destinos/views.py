from typing import Any
from django import http
from django.shortcuts import render
from django.http import HttpRequest, JsonResponse, HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from back.models import *
from back.forms import *
from web.models import *
from django.shortcuts import render
from django.http import HttpResponse
import csv
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_GET
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404
#serializers
# render to string
from django.template.loader import render_to_string
from django.utils.decorators import method_decorator
# para archivo excel
from django.views import View
from django.contrib import messages
from openpyxl import load_workbook
import csv
import os
import datetime
from django.urls import reverse
import openpyxl
from django.http import HttpResponse
import json
from config.diccionarios import clean_str_col, homologar_columna_categoria, homologar_columna_destino


def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'


class FuenteInfoPerfilVisitanteDestinos (ListView):
    model = FuenteInfoPerfilVisitanteDestino
    template_name = 'back/fuente_info_perfil_visitante_destinos/viewer.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs) :
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search':
                data = []
                for i in FuenteInfoPerfilVisitanteDestino.objects.all():
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Fuentes de Información de PV Destinos'
        context['create_url'] = reverse_lazy('dashboard:fuente_info_perfil_visitante_destinos_create')
        context['entity'] = 'Fuentes de Información de PV Eventos'
        context['is_fuente'] = True

        return context  
    
class FuenteInfoPerfilVisitanteDestinosCreate(CreateView):

    model = FuenteInfoPerfilVisitanteDestino    

    form_class = FuenteInfoPerfilVisitanteDestinoForm
    template_name = 'back/fuente_info_perfil_visitante_destinos/create.html'
    success_url = reverse_lazy('dashboard:fuente_info_perfil_visitante_destinos')

    def get_object(self, **kwargs):
        queryset = self.get_queryset()
        try:
            return queryset.get(**kwargs)
        except queryset.model.DoesNotExist:
            return None

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        replace_data = request.POST.get('replace_data')
        if form.is_valid():
            # Check if there is already a record with the same fecha, destino and categoria

            fecha = form.cleaned_data['fecha']
            ano = form.cleaned_data['ano']
            destino = form.cleaned_data['destino']


            try:
                existing_object = self.get_object(fecha=fecha, destino=destino, ano=ano)

            except FuenteInfoPerfilVisitanteEvento.DoesNotExist:
                existing_object = None

            existing_catalogo = CatalagoDestino.objects.filter(destino=destino).exists()
            # ALTER TABLE mytable MODIFY mycolumn VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

            # If there is no existing data, save the new data
            if not existing_catalogo:

                if not existing_catalogo:
                    data = {
                        'success': False,
                        'missingData': True,
                        'destino': destino,
                        'message': 'No existe el la entidad en el catalogo',
                    }
                    return JsonResponse(data)

            # If there is existing data and replace_data is True, delete the existing data
            if existing_object and request.POST.get('replace_data') == 'on':
                # existing_object.delete()
                # Save the new data
                # self.object = form.save()

                for field in form.cleaned_data:
                    if field == 'replace_data':
                        continue
                    setattr(existing_object, field, form.cleaned_data[field])

                existing_object.save()

                data = {
                    'success': True,
                    'message': 'Data created successfully.',
                    'url': self.success_url,

                }
                return JsonResponse(data)

            # If there is existing data and replace_data is False, return an error

            if existing_object:
                data =  FuenteInfoPerfilVisitanteDestino.objects.filter(fecha=fecha, destino=destino, ano=ano)
                data_list = list(data.values( 'ano',
    'folio',
    'herramienta',
    'fecha',
    'temporada',
    'destino',
    'residencia',
    'tipo_asistente',
    'municipio',
    'estado',
    'pais',
    'origen',
    'motivo_visita',
    'motivo_visita_otro',
    'segmento',
    'tipo_hospedaje',
    'tipo_visitante',
    'estadia_dias',
    'estadia_hrs',
    'acompanantes',
    'acompanantes_maxmin',
    'medio_transporte_edo',
    'tiene_fam',
    'visita_fam',
    'sat_hospedaje',
    'sat_ayb',
    'sat_atractivos',
    'sat_tours',
    'sat_central',
    'sat_aeropuerto',
    'sat_carretera',
    'sat_infotur',
    'sat_estacionamiento',
    'sat_hospitalidad',
    'sat_seguridad',
    'sat_experiencia',
    'sat_accesibilidad',
    'sat_senaletica',
    'sat_transporte',
    'sat_limpieza',
    'sat_eventos',
    'sat_protocolos',
    'sat_precios',
    'recomendacion_destino',
    'retorno_destino',
    'nps_destino',
    'nps_destino_categoria',
    'nps_hotel',
    'nps_ayb',
    'nps_atractivos',
    'nps_tours',
    'vio_escucho_noticias',
    'impacto_noticias',
    'identifico_practicas_sust',
    'edad',
    'nse',
    'sexo',
    'proposito_visita_destino_estado',
    'codigo_encuesta_ano',
    ))
                data_list2 = list(form.cleaned_data.values())
                table_html = render_to_string('back/fuente_info_perfil_visitante_destinos/table.html',{'data_list': data_list, 'actual': True, 'data_list2': data_list2})

                datajsn = {
                    'success': False,
                    'message': 'Hubo un error al crear registro.',
                    'errors': 'Ya existe un registro con la misma fecha, destino , origen y museo o zona arqueologica',
                    'existing_object': table_html
                }

                return JsonResponse(datajsn)
            else:
                self.object = form.save()
                data = {
                    'success': True,
                    'message': 'Data created successfully.',
                    'url': self.success_url
                }
                return JsonResponse(data)
        else:
            data = {
                'success': False,
                'message': 'Error creating data.',
                'errors': form.errors,
                'format_errors': True
            }
            return JsonResponse(data)

    def form_invalid(self, form):
        response = super().form_invalid(form)
        data = {
            'success': False,
            'message': 'Hubo un error al crear registro.',
            'errors': form.errors
        }
        return JsonResponse(data)

    def form_valid(self, form):
        response = super().form_valid(form)
        data = {
            'success': True,
            'message': 'Registro creado exitosamente.',
            'url': self.success_url
        }
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Crear Fuente de Información de PV Destinos'
        context['entity'] = 'Fuentes de Información de PV Destinos'
        context['list_url'] = reverse_lazy('dashboard:fuente_info_perfil_visitante_destinos')
        context['action'] = 'add'
        return context
    

class FuenteInfoPerfilVisitanteDestinosUpdate(UpdateView):
    model = FuenteInfoPerfilVisitanteDestino
    form_class = FuenteInfoPerfilVisitanteDestinoForm
    template_name = 'back/fuente_info_perfil_visitante_destinos/create.html'
    success_url = reverse_lazy('dashboard:fuente_info_perfil_visitante_destinos')

    def form_invalid(self, form):
        response = super().form_invalid(form)
        data = {
            'success': False,
            'message': 'Hubo un error al subir los datos.',
            'errors': form.errors
        }
        if is_ajax(self.request):
            return JsonResponse(data)
        else:
            return response

    def form_valid(self, form):
        response = super().form_valid(form)
        data = {
            'success': True,
            'message': 'Fuente creada exitosamente.',
            'url': self.success_url
        }
        if is_ajax(self.request):
            return JsonResponse(data)
        else:
            return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['list_url'] = reverse_lazy('dashboard:fuente_info_perfil_visitante_destinos')
            # Set the widget for the 'destino' field to read-only text input
        context['form'].fields['ano'].widget = forms.TextInput(attrs={'readonly': 'readonly'})
        context['form'].fields['folio'].widget = forms.TextInput(attrs={'readonly': 'readonly'})
        context['form'].fields['fecha'].widget = forms.TextInput(attrs={'readonly': 'readonly'})
        context['form'].fields['destino'].widget = forms.TextInput(attrs={'readonly': 'readonly'})
  
        context['title'] = 'Editar fuente de información de PV Destinos'

        context['edit_msg'] = 'Los Campos año , folio, fecha, destino y nombre_evento no se pueden editar'

        return context


class FuenteInfoPerfilVisitanteDestinosDelete(DeleteView):
    model = FuenteInfoPerfilVisitanteDestino
    success_url = reverse_lazy('dashboard:fuente_info_perfil_visitante_destinos')
    
    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        return super().post(request, *args, **kwargs)
