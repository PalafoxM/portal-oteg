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
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'\
    

class ModiuloConfigDestinos (ListView):
    model = CatalagoDestino
    template_name  =  'back/modulo_config_destinos/viewer.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado  Modulo Config Destinos'
        context['create_url'] = reverse_lazy('dashboard:configuracion_destinos_create')
        context['entity'] = 'Destino'
        return context  
    

class ModiuloConfigDestinosCreateView (CreateView):
    model = CatalagoDestino
    form_class = CatalogoDestinoForm
    template_name = 'back/modulo_config_destinos/create.html'
    success_url = reverse_lazy('dashboard:configuracion_destinos_list')

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
            destino = form.cleaned_data['destino'].lower()
            try:
                existing_object = self.get_object(destino=destino)

            except Sesibilizacion.DoesNotExist:
                existing_object = None

            if existing_object:

                datajsn = {
                    'success': False,
                    'message': 'Hubo un error al crear registro.',
                    'errors': 'Ya existe un registro con la mima informacion.',
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
        context['title'] = 'Crear  Modulo Config Destinos'
        context['list_url'] = reverse_lazy('dashboard:configuracion_destinos_list')
        context['action'] = 'add'
        return context


class ModiuloConfigDestinosUpdateView (UpdateView):

    model = CatalagoDestino
    form_class = CatalogoDestinoForm
    template_name = 'back/modulo_config_destinos/create.html'
    success_url = reverse_lazy('dashboard:configuracion_destinos_list')

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
        context['list_url'] = reverse_lazy('dashboard:configuracion_destinos_list')
        context['title'] = 'Editar Modulo Config Destinos'

        return context
    
class ModiuloConfigDestinosDeleteView  (DeleteView):
    model = CatalagoDestino
    success_url = reverse_lazy('dashboard:configuracion_destinos_list')

    

    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        return super().post(request, *args, **kwargs)

