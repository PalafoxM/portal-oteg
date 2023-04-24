from django.shortcuts import render
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse_lazy , reverse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from back.models import  *
from back.forms import *
from web.models import *
from django.shortcuts import render
from django.http import HttpResponse
import csv
import pandas as pd
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_GET
from django.views.decorators.http import require_POST


def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'



class FuenteInfoGastoDerrama (ListView):
    model = GastoDerrama
    template_name = 'back/fuente_info_gasto_derrama/viewer.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Fuentes de Informacion Gasto Derrama'
        context['create_url'] = reverse_lazy('dashboard:fuente_info_gasto_derrama_create')
        context['entity'] = 'Categorias'
        context['is_fuente']    = True
        return context
    
class FuenteInfoGastoDerramaCreate (CreateView):
    model = GastoDerrama
    form_class = GastoDerramaForm
    template_name ='back/components/create_update.html'
    success_url = reverse_lazy('dashboard:fuente_info_gasto_derrama')

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            self.object = form.save()
            data = {
                'success': True,
                'message': 'fuente Creada exitosamente.',
                'url': self.success_url
            }
            return JsonResponse(data)
        else:
            data = {
                'success': False,
                'message': 'Hubo un error al crear registro.',
                'errors': form.errors
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
        context['list_url'] = reverse_lazy('dashboard:fuente_info_gasto_derrama')
        context['action'] = 'add'
        return context
    

class FuenteInfoGastoDerramaUpdate (UpdateView):
    model = GastoDerrama
    form_class = GastoDerramaForm
    template_name = 'back/components/create_update.html'
    success_url = reverse_lazy('dashboard:fuente_info_gasto_derrama')

    def form_invalid(self, form):
        response = super().form_invalid(form)
        data = {
            'success': False,
            'message': 'Hubo un error al crear el evento.',
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
            'message': 'Evento creado exitosamente.',
            'url': self.success_url
        }
        if is_ajax(self.request):
            return JsonResponse(data)
        else:
            return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.form_class(instance=self.object)
        context['list_url'] = reverse_lazy('dashboard:fuente_info_gasto_derrama')
        return context
    
class FuenteInfoGastoDerramaDelete(DeleteView):
    model = GastoDerrama
    success_url = reverse_lazy('dashboard:fuente_info_gasto_derrama')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.delete()
        return HttpResponseRedirect(success_url)