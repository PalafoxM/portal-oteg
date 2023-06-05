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

class FuenteInfoEntornoNacional (ListView):
    model = FuenteInfoEntornoN 
    form_class = FuenteInfoEntornoNForm
    template_name = 'back/fuente_info_entorno_nacional/viewer.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs) :
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search':
                data = []
                for i in FuenteInfoEntornoN.objects.all():
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Fuentes de Informacion Nacional'
        context['create_url'] = reverse_lazy('dashboard:fuente_info_entorno_nacional_create')
        context['entity'] = 'Nacional'
        context['is_fuente'] = True
        return context  
    
class FuenteInfoEntornoNacionalCreate(CreateView):
    model = FuenteInfoEntornoN
    form_class = FuenteInfoEntornoNForm
    template_name = 'back/fuente_info_entorno_nacional/create.html'
    success_url = reverse_lazy('dashboard:fuente_info_entorno_nacional')

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
            entidad = form.cleaned_data['entidad']

            try:
                existing_object = self.get_object(fecha=fecha, entidad=entidad)

            except Certificacion.DoesNotExist:
                existing_object = None

            existing_catalogo = CatalogoEntidad.objects.filter(entidad__iexact= entidad).exists()
            # ALTER TABLE mytable MODIFY mycolumn VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

            # If there is no existing data, save the new data
            if not existing_catalogo:

                if not existing_catalogo:
                    data = {
                        'success': False,
                        'missingData': True,
                        'destino': entidad,
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
                data = FuenteInfoEntornoN.objects.filter(fecha=fecha, entidad=entidad)

                data_list = list(data.values('entidad', 'fecha', 'cuartos_disponibles_promedio', 'cuartos_disponibles','cuartos_ocupados','cuartos_ocupados_nacionales','cuartos_ocupados_extranjeros' ,'cuartos_ocupados_sin_clasificar',
    'llegada_de_turistas',
    'llegada_de_turistas_nacionales',
    'llegada_de_turistas_extranjeros',
    'turistas_noche',
    'turistas_noche_nacionales',
    'turistas_noche_extranjeros',
    'porcentaje_de_ocupacion',
    'porcentaje_de_ocupacion_nacionales',
    'porcentaje_de_ocupacion_extranjeros',
    'porcentaje_de_ocupacion_sin_clasificar',
    'densidad',
    'densidad_nacionales',
    'densidad_extranjeros',
    'estadia_promedio',
    'estadia_promedio_nacionales',
    'estadia_promedio_extranjeros' 
    ))
                data_list2 = list(form.cleaned_data.values())
                table_html = render_to_string('back/fuente_info_entorno_nacional/table.html',{'data_list': data_list, 'actual': True, 'data_list2': data_list2})

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
        context['title'] = 'Crear una fuente'
        context['entity'] = 'Glosario'
        context['list_url'] = reverse_lazy('dashboard:fuente_info_entorno_nacional')
        context['action'] = 'add'
        return context



class FuenteInfoEntornoNacionalUpdate (UpdateView):
    model =     FuenteInfoEntornoN
    form_class = FuenteInfoEntornoNForm
    template_name = 'back/fuente_info_entorno_nacional/create.html'
    success_url = reverse_lazy('dashboard:fuente_info_entorno_nacional')

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
        context['list_url'] = reverse_lazy('dashboard:fuente_info_entorno_nacional')
            # Set the widget for the 'destino' field to read-only text input
        context['form'].fields['fecha'].widget = forms.TextInput(attrs={'readonly': 'readonly'})
        context['form'].fields['entidad'].widget = forms.TextInput(attrs={'readonly': 'readonly'})
        context['title'] = 'Editar fuente'

        context['edit_msg'] = 'Los Campos Destino y Fecha no pueden ser editados' 

        return context
    
class FuenteInfoEntornoNacionalDelete (DeleteView):
    model = FuenteInfoEntornoN
    success_url = reverse_lazy('dashboard:fuente_info_entorno_nacional')
    
    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        return super().post(request, *args, **kwargs)