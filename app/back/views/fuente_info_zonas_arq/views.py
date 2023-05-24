from django.shortcuts import render
from django.http import JsonResponse, HttpResponseRedirect
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
from django.template.loader import render_to_string


def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'


class FuenteInfoZonasArqueologicas (ListView):
    model = zonas_arqueologicas_museos
    template_name = 'back/fuente_info_zonas_arq/viewer.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Fuentes de Informacion Zonas Arqueologicas'
        context['create_url'] = reverse_lazy(
            'dashboard:fuente_info_zonas_arqueologicas_create')
        context['entity'] = 'Zonas Arqueologicas'
        context['is_fuente'] = True
        return context


class FuenteInfoZonasArqueologicasCreate (CreateView):
    model = zonas_arqueologicas_museos
    form_class = ZonasArqueologicasMuseosForm
    template_name = 'back/fuente_info_zonas_arq/create.html'    
    success_url = reverse_lazy('dashboard:fuente_info_zonas_arqueologicas')

    def get_object(self, **kwargs):
        queryset = self.get_queryset()
        try:
            return queryset.get(**kwargs)
        except queryset.model.DoesNotExist:
            return None

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            # Check if there is already a record with the same fecha, destino and categoria

            fecha = form.cleaned_data['fecha']
            destino = form.cleaned_data['destino']
            origen = form.cleaned_data['origen_visitante']
            nombre = form.cleaned_data['nombre']

            try:
                existing_object = self.get_object(fecha=fecha, destino=destino, origen_visitante=origen, nombre=nombre)

            except DataTour.DoesNotExist:
                existing_object = None

            catalogo_destino = CatalagoDestino.objects.filter(destino=destino).exists()
            catalogo_museo_zona_arqueologica = CatalagoZAMuseos.objects.filter(nombre=nombre).exists()
            print("destino",catalogo_destino)
            print("ZA",catalogo_museo_zona_arqueologica)


            # If there is no existing data, save the new data
            if not catalogo_museo_zona_arqueologica or not destino:
          
                if not catalogo_museo_zona_arqueologica and not catalogo_destino:

                    print("no existe nada")

                    data = {
                        'success': False,
                        'missingData': True,
                        'museo_Z_A': nombre,
                        'destino': destino,
                        'message': 'No existe la categoria o el destino en el catalogo',
                    }
                    return JsonResponse(data)

                if not catalogo_museo_zona_arqueologica:
                    data = {
                        'success': False,
                        'missingData': True,
                        'museo_Z_A': nombre,
                        'message': 'No existe la Zona Arqueologica o Museo en el catalogo',
                    }
                    return JsonResponse(data)

                if not catalogo_destino:
                    data = {
                        'success': False,
                        'missingData': True,
                        'destino': destino,
                        'message': 'No existe el destino en el catalogo',
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
                data = zonas_arqueologicas_museos.objects.filter(fecha=fecha, destino=destino, origen_visitante=origen, nombre=nombre)

                data_list = list(data.values('destino','tipo','nombre', 'fecha', 'origen_visitante', 'visitantes'))   
                data_list2 = list(form.cleaned_data.values())
                table_html = render_to_string('back/fuente_info_zonas_arq/table.html', {'data_list': data_list, 'actual': True, 'data_list2': data_list2})

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
        context['list_url'] = reverse_lazy('dashboard:fuente_info_zonas_arqueologicas')
        context['action'] = 'add'
        return context

class FuenteInfoZonasArqueologicasUpdate (UpdateView):
    model = zonas_arqueologicas_museos
    form_class = ZonasArqueologicasMuseosForm_edit
    template_name = 'back/fuente_info_zonas_arq/view_editor.html'
    success_url = reverse_lazy('dashboard:fuente_info_zonas_arqueologicas')

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
        context['list_url'] = reverse_lazy('dashboard:fuente_info_zonas_arqueologicas')
            # Set the widget for the 'destino' field to read-only text input
        context['form'].fields['destino'].widget = forms.TextInput(attrs={'readonly': 'readonly'})
        # Set the widget for the 'fecha' field to read-only text input
        context['form'].fields['nombre'].widget = forms.TextInput(attrs={'readonly': 'readonly'})
        # Set the widget for the 'categoria' field to read-only text input
        context['form'].fields['fecha'].widget = forms.TextInput(attrs={'readonly': 'readonly'})
        # Set the widget for the 'categoria' field to read-only text input
        context['form'].fields['origen_visitante'].widget = forms.TextInput(attrs={'readonly': 'readonly'})

        context['title'] = 'Editar fuente'
        context['edit_msg'] = 'Los Campos Destino, Fecha, Museo o Zona Arqueologica y Origen Visitante no pueden ser editados' 

        return context

class FuenteInfoZonasArqueologicasDelete (DeleteView):
    model = zonas_arqueologicas_museos
    success_url = reverse_lazy('dashboard:fuente_info_zonas_arqueologicas')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.delete()
        return HttpResponseRedirect(success_url)

