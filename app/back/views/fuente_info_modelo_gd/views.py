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
from django.contrib.auth.decorators import login_required, permission_required
from django.utils.decorators import method_decorator
from django.http import Http404
from django.core.exceptions import PermissionDenied

from django.contrib.auth.decorators import user_passes_test

def es_admin_o_superadmin(user):
    return user.is_authenticated and (user.is_staff or user.is_superuser)


def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'


@method_decorator(login_required(login_url='/auth/login_user'), name='dispatch')
@method_decorator(permission_required('auth.view_banner', raise_exception=True), name='dispatch')
@method_decorator(user_passes_test(es_admin_o_superadmin, login_url='404'), name='dispatch')
class FuenteInfoModeloGD (ListView):
    model = ModeloGD
    template_name = 'back/fuente_info_Modelo_GD/viewer.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Fuentes de Informacion de Modelo GD'
        context['create_url'] = reverse_lazy('dashboard:fuente_info_modelo_gd_create')
        context['entity'] = 'ModeloGD'
        context['is_fuente'] = True
        
        return context

@method_decorator(login_required(login_url='/auth/login_user'), name='dispatch')
@method_decorator(permission_required('auth.view_banner', raise_exception=True), name='dispatch')
@method_decorator(user_passes_test(es_admin_o_superadmin, login_url='404'), name='dispatch')    
class FuenteInfoModeloGDCreate (CreateView):
    model = ModeloGD
    form_class = ModeloGDForm
    template_name = 'back/fuente_info_Modelo_GD/create.html'
    success_url = reverse_lazy('dashboard:fuente_info_modelo_gd')

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

            anio = form.cleaned_data['anio']
            destino = form.cleaned_data['destino']


            try:
                existing_object = self.get_object(anio=anio, destino=destino)

            except ModeloGD.DoesNotExist:
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
                data = ModeloGD.objects.filter(anio=anio, destino=destino)

                data_list = list(data.values('anio','destino','gasto_diario_promedio','participacion','estadia_promedio'))
                data_list2 = list(form.cleaned_data.values())
                table_html = render_to_string('back/fuente_info_Modelo_GD/table.html',{'data_list': data_list, 'actual': True, 'data_list2': data_list2})

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
        context['entity'] = 'ModeloGD'
        context['list_url'] = reverse_lazy('dashboard:fuente_info_modelo_gd')
        context['action'] = 'add'
        return context

@method_decorator(login_required(login_url='/auth/login_user'), name='dispatch')
@method_decorator(permission_required('auth.view_banner', raise_exception=True), name='dispatch')
@method_decorator(user_passes_test(es_admin_o_superadmin, login_url='404'), name='dispatch')    
class FuenteInfoModeloGDUpdate (UpdateView):
    model = ModeloGD
    form_class = ModeloGDForm
    template_name = 'back/fuente_info_Modelo_GD/create.html'
    success_url = reverse_lazy('dashboard:fuente_info_modelo_gd')

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
        context['list_url'] = reverse_lazy('dashboard:fuente_info_modelo_gd')
            # Set the widget for the 'destino' field to read-only text input
        context['form'].fields['destino'].widget = forms.TextInput(attrs={'readonly': 'readonly'})

        context['form'].fields['anio'].widget = forms.TextInput(attrs={'readonly': 'readonly'})
        context['title'] = 'Editar fuente'

        context['edit_msg'] = 'Los Campos Destino y Año no pueden ser editados' 

        return context

@method_decorator(login_required(login_url='/auth/login_user'), name='dispatch')
@method_decorator(permission_required('auth.view_banner', raise_exception=True), name='dispatch')
@method_decorator(user_passes_test(es_admin_o_superadmin, login_url='404'), name='dispatch')    
class FuenteInfoModeloGDDelete (DeleteView):
    model = ModeloGD
    success_url = reverse_lazy('dashboard:fuente_info_modelo_gd')
        
    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        return super().post(request, *args, **kwargs)

