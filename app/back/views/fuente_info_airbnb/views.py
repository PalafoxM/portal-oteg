from typing import Any, Dict
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
from django.template.loader import render_to_string


def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'


class FuenteInfoAirbnb (ListView):
    model = Airbnb
    template_name = 'back/fuente_info_airbnb/viewer.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Fuentes de Informacion Airbnb'
        context['create_url'] = reverse_lazy('dashboard:fuente_info_airbnb_create')
        context['entity'] = 'Airbnb'
        context['is_fuente'] = True
        return context

class FuenteInfoAirbnbCreate (CreateView):
    model = Airbnb
    form_class = AirbnbForm
    template_name = 'back/fuente_info_airbnb/create.html'
    success_url = reverse_lazy('dashboard:fuente_info_airbnb')

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
            fechaI = form.cleaned_data['fecha_inicio']
            destino = form.cleaned_data['destino']
            fechaF = form.cleaned_data['fecha_fin']

            try:
                existing_object = self.get_object(fecha_inicio=fechaI, destino=destino, fecha_fin=fechaF)

            except Certificacion.DoesNotExist:
                existing_object = None

            existing_catalogo = CatalagoDestino.objects.filter(destino__iexact=destino).exists()
            # ALTER TABLE mytable MODIFY mycolumn VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

            # If there is no existing data, save the new data
            if not existing_catalogo:

                if not existing_catalogo:
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
                data =  Airbnb.objects.filter(fecha_inicio=fechaI, destino=destino, fecha_fin=fechaF)

                data_list = list(data.values( 'fecha_inicio', 'fecha_fin' , 'destino', 'propiedad_renta','porcentaje_ocupacion','tarifa_promedio'))
                data_list2 = list(form.cleaned_data.values())
                table_html = render_to_string('back/fuente_info_airbnb/table.html',{'data_list': data_list, 'actual': True, 'data_list2': data_list2})

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
        context['list_url'] = reverse_lazy('dashboard:fuente_info_airbnb')
        context['action'] = 'add'
        return context


class FuenteInfoAirbnbUpdate (UpdateView): 
    model = Airbnb
    form_class = AirbnbForm
    template_name = 'back/fuente_info_airbnb/create.html'
    success_url = reverse_lazy('dashboard:fuente_info_airbnb')

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
        context['list_url'] = reverse_lazy('dashboard:fuente_info_airbnb')
            # Set the widget for the 'destino' field to read-only text input
        context['form'].fields['destino'].widget = forms.TextInput(attrs={'readonly': 'readonly'})
        # Set the widget for the 'fecha' field to read-only text input
        context['form'].fields['fecha_inicio'].widget = forms.TextInput(attrs={'readonly': 'readonly'})
        # Set the widget for the 'categoria' field to read-only text input
        context['form'].fields['fecha_fin'].widget = forms.TextInput(attrs={'readonly': 'readonly'})
        context['title'] = 'Editar fuente'
        context['edit_msg'] = 'Los Campos Fecha Inicio , Destino y Fecha Fin no se pueden editar'

        return context
    

class FuenteInfoAirbnbDelete (DeleteView):
    model = Airbnb
    success_url = reverse_lazy('dashboard:fuente_info_airbnb')
    
    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        return super().post(request, *args, **kwargs)
