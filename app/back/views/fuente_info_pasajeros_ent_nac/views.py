from typing import Any, Dict
from django.shortcuts import render
from django.http import HttpRequest, JsonResponse, HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from back.models import *
from back.forms import *
from web.models import *
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.template.loader import render_to_string
# para archivo excel
from django.views import View
from django.contrib import messages
from openpyxl import load_workbook
import csv
import os
from datetime import datetime
from django.urls import reverse
import openpyxl
from django.http import HttpResponse
import json
from config.diccionarios import clean_str_col, homologar_columna_categoria, homologar_columna_destino


def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'


class FuenteInfoPasajerosEntNacView(ListView):
    model = Pasajeros_Ent_Nac
    template_name = 'back/pasajeros_ent_nac/viewer.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Fuentes de Informacion de Pasajeros Entrada Nacional'
        context['create_url'] = reverse_lazy(
            'dashboard:fuente_info_pasajeros_ent_nac_create')
        context['entity'] = 'Fuentes de Informacion de Pasajeros Entrada Nacional'
        context['is_fuente'] = True
        return context


class FuenteInfoPasajerosEntNacCreate(LoginRequiredMixin, CreateView):
    model = Pasajeros_Ent_Nac
    form_class = PasajerosEntNacForm
    template_name = 'back/pasajeros_ent_nac/create.html'
    success_url = reverse_lazy('dashboard:fuente_info_pasajeros_ent_nac')

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

            aereopuerto = form.cleaned_data['aereopuerto']
            entidad = form.cleaned_data['entidad']
            ano = form.cleaned_data['ano']

            try:
                existing_object = self.get_object(
                    aereopuerto=aereopuerto, entidad=entidad, ano=ano)

            except Certificacion.DoesNotExist:
                existing_object = None

            existing_catalogo = CatalogoAeropuertos.objects.filter(aereopuerto__iexact=aereopuerto).exists()
            existing_catalogo2 = CatalogoAeropuertos.objects.filter(
                entidad__iexact=entidad).exists()
            # ALTER TABLE mytable MODIFY mycolumn VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

            # If there is no existing data, save the new data
            if not existing_catalogo or not existing_catalogo2:

                if not existing_catalogo and not existing_catalogo2:
                    data = {
                        'success': False,
                        'missingData': True,
                        'destino': aereopuerto,
                        'categoria': entidad,
                        'message': 'No existe el aeropuerto ni la entidad en el catalogo',
                    }
                    return JsonResponse(data)

                if not existing_catalogo:
                    data = {
                        'success': False,
                        'missingData': True,
                        'destino': aereopuerto,
                        'message': 'No existe el aeropuerto en el catalogo',
                    }
                    return JsonResponse(data)

                if not existing_catalogo2:
                    data = {
                        'success': False,
                        'missingData': True,
                        'categoria': entidad,
                        'message': 'No existe la entidad en el catalogo',
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
                data = Pasajeros_Ent_Nac.objects.filter(
                    aereopuerto=aereopuerto, entidad=entidad, ano=ano)

                data_list = list(data.values('aereopuerto', 'entidad', 'ano', 'nacionales', 'regulares', 'nacionales_regulares',
                                             'internacionales_regulares', 'charters', 'charters_nacionales', 'charters_internacionales'))

                data_list2 = list(form.cleaned_data.values())
                table_html = render_to_string('back/pasajeros_ent_nac/table.html', {
                                              'data_list': data_list, 'actual': True, 'data_list2': data_list2})

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
        context['list_url'] = reverse_lazy('dashboard:fuente_info_pasajeros_ent_nac')
        context['action'] = 'add'
        return context


class FuenteInfoPasajerosEntNacUpdate (UpdateView):
    model = Pasajeros_Ent_Nac
    form_class =    PasajerosEntNacForm
    template_name = 'back/fuente_info_certificacion/view_editor.html'
    success_url = reverse_lazy('dashboard:fuente_info_certificacion')

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

        context['list_url'] = reverse_lazy('dashboard:fuente_info_pasajeros_ent_nac')
        # Set the widget for the 'destino' field to read-only text input

        context['form'].fields['ano'].widget = forms.TextInput(attrs={'readonly': 'readonly'})
        context['form'].fields['aereopuerto'].widget = forms.TextInput(attrs={'readonly': 'readonly'})
        context['form'].fields['entidad'].widget = forms.TextInput(attrs={'readonly': 'readonly'})

        context['title'] = 'Editar fuente de informacion'

        context['edit_msg'] = 'Los Campos Año , Aeropuerto y Entidad no se pueden editar'
        return context



class FuenteInfoPasajerosEntNacDelete (DeleteView):
    model = Pasajeros_Ent_Nac
    success_url = reverse_lazy('dashboard:fuente_info_pasajeros_ent_nac')
    
    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        return super().post(request, *args, **kwargs)
