from django.shortcuts import render, redirect
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView , TemplateView
from django.urls import reverse_lazy
from back.models import  *
from back.forms import *
from django.http import JsonResponse, HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views import View
from django.contrib import messages
from openpyxl import load_workbook
import csv
import os
import datetime
from django.urls import reverse
import openpyxl
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.views.decorators.http import require_GET
import json
from config.diccionarios import clean_str_col, homologar_columna_categoria, homologar_columna_destino
from django.shortcuts import get_object_or_404
from django.http import Http404
from django.db.models import Q
from django.contrib.auth.decorators import login_required, permission_required
from django.utils.decorators import method_decorator
from django.http import Http404
from django.core.exceptions import PermissionDenied
from back.mixins import *
from django.contrib.auth.decorators import user_passes_test

def es_admin_o_superadmin(user):
    return user.is_authenticated and (user.is_staff or user.is_superuser)


# Create your views here.
def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'



class ReporteView(SuperAdminOrAdminMixin, LoginRequiredMixin, ListView):
    model = Report
    template_name = 'back/modulo_reportes/viewer.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Reportes'
        context['d_route'] = 'Estadísticas > Reportes'
        context['create_url'] = reverse_lazy('dashboard:reporte_create')
        context['entity'] = 'Reportes'
    
        return context



class ReporteCreate(CreateView):
    model = Report
    form_class = ReportsForm
    template_name = 'back/modulo_reportes/create_update.html'
    success_url = reverse_lazy('dashboard:modulo_reportes')

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            self.object = form.save()
            data = {
                'success': True,
                'message': 'Reporte creado exitosamente.',
                'url': self.success_url
            }
            return JsonResponse(data)
        else:
            data = {
                'success': False,
                'message': 'Hubo un error al crear el evento.',
                'errors': form.errors
            }
            return JsonResponse(data)

    def form_invalid(self, form):
        response = super().form_invalid(form)
        data = {
            'success': False,
            'message': 'Hubo un error al crear el evento.',
            'errors': form.errors
        }
        return JsonResponse(data)

    def form_valid(self, form):
        response = super().form_valid(form)
        data = {
            'success': True,
            'message': 'Reporte creado exitosamente.',
            'url': self.success_url
        }
        return JsonResponse(data)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Crear una Reporte'
        context['entity'] = 'Reportes'
        context['list_url'] = reverse_lazy('dashboard:modulo_reportes')
        context['action'] = 'add'
        context['d_route'] = 'Estadísticas > Reportes'
        return context
    


class ReporteUpdate(UpdateView):
    model = Report
    form_class = ReportsForm
    template_name = 'back/modulo_reportes/create_update.html'
    success_url = reverse_lazy('dashboard:modulo_reportes')

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
        context['list_url'] = reverse_lazy('dashboard:modulo_reportes')
        context['d_route'] = 'Estadísticas > Reportes'
        return context 
    


    
class ReporteDelete(DeleteView):
    model = Report
    # template_name = 'back/delete.html'
    success_url = reverse_lazy('dashboard:modulo_reportes')
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        try:
            self.object.delete()
            return JsonResponse({'message': 'Eliminación exitosa.'})
        except Exception as e:
            return JsonResponse({'error': 'Error al eliminar el registro.'}, status=500)
    


class ReporteDetail (TemplateView):
    model = Report
    template_name = 'back/modulo_reportes/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try : 
            s = get_object_or_404(Report, id=self.kwargs.get('pk'))
        except :
            raise Http404("No existe la seccion")
    
        context['report'] = s

        return context
    

@require_GET
def get_reports(request):
    q = request.GET.get('q', '')

    results = Report.objects.filter(~Q(nomenclatura__icontains='OTEG'))
    # results = Report.objects.all()
    data = [{'titulo': obj.nomenclatura, 'id': obj.id } for obj in results]
    return JsonResponse(data, safe=False)
