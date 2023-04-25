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
import pandas as pd
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




def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'


class FuenteInfoDatatur (ListView):
    model = DataTour
    template_name = 'back/fuente_info_datatur/viewer.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Fuentes de Informacion de DataTour'
        context['create_url'] = reverse_lazy(
            'dashboard:fuente_info_datatour_create')
        context['entity'] = 'Categorias'
        context['is_fuente'] = True
        return context


class FuenteInfoDataturCreate (CreateView):
    model = DataTour
    form_class = DataTurForm
    template_name = 'back/components/create_update_fuentes_info.html'
    success_url = reverse_lazy('dashboard:fuente_info_datatour')

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
            destino = form.cleaned_data['destino']
            categoria = form.cleaned_data['categoria']
            try:
                existing_object = self.get_object(fecha=fecha, destino=destino, categoria=categoria)
             

            except DataTour.DoesNotExist:
                existing_object = None 

            existing_category = catalogo_categorias.objects.filter(categoria=categoria).exists()
            existing_catalogo = catalogo_destinos.objects.filter(destino=destino).exists()

            if request.POST.get('catalog') == 'on':
                if not existing_category:
                    catalogo_categorias.objects.create(categoria=categoria)
                if not existing_catalogo:
                    catalogo_destinos.objects.create(destino=destino)

                self.object = form.save()
                
                data = {
                    'success': True,
                    'message': 'Data created successfully.',
                    'url': self.success_url
                }
                return JsonResponse(data)
                


            # If there is no existing data, save the new data
            if not existing_category or not existing_catalogo:

                if not existing_category and not existing_catalogo:
    
                    data = {
                        'success': False,
                        'missingData': True,
                        'categoria': categoria,
                        'destino': destino, 
                        'message': 'No existe la categoria o el destino en el catalogo',
                    }
                    return JsonResponse(data)
                
                if not existing_category:
                    data = {
                        'success': False,
                        'missingData': True,
                        'categoria': categoria,
                        'message': 'No existe la categoria en el catalogo',
                    }
                    return JsonResponse(data)
                
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
                #existing_object.delete()
                # Save the new data
                #self.object = form.save()

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

            if existing_object  :
                data = DataTour.objects.filter(fecha=fecha, destino=destino, categoria=categoria)
                
                data_list = list(data.values('fecha', 'destino', 'categoria','cuartos_registrados', 'cuartos_disponibles', 'cuartos_disponibles_prom' ,'cuartos_ocupados','cuartos_ocupados_residentes','cuartos_ocupados_no_residentes','llegadas_turistas','llegadas_turistas_residentes','llegadas_turistas_no_residentes','turistas_noche','turistas_noche_residentes', 'turistas_noche_no_residentes','porcentaje_ocupacion','porcentaje_ocupacion_residentes','porcentaje_ocupacion_no_residentes','estadia_promedio','estadia_promedio_residentes','estadia_promedio_no_residentes','densidad_ocupacion','densidad_ocupacion_residentes','densidad_ocupacion_no_residentes','fecha_recuperacion'))                                                 
                data_list2 =  list(form.cleaned_data.values())
                table_html = render_to_string('back/fuente_info_datatur/data_tour_table.html', {'data_list': data_list , 'actual':True , 'data_list2':data_list2})                            
                
                datajsn = {
                        'success': False,
                        'message': 'Hubo un error al crear registro.',
                        'errors': 'Ya existe un registro con la misma fecha, destino y categoria.',
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
                'format_errors':True
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
        context['list_url'] = reverse_lazy('dashboard:fuente_info_datatour')
        context['action'] = 'add'
        return context

class FuenteInfoDataturUpdate(UpdateView):
    
    model = DataTour
    form_class = DataTurForm
    template_name = 'back/components/create_update_fuentes_info.html'
    success_url = reverse_lazy('dashboard:fuente_info_datatour')

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
        context['list_url'] = reverse_lazy('dashboard:fuente_info_datatour')
            # Set the widget for the 'destino' field to read-only text input
        context['form'].fields['destino'].widget = forms.TextInput(attrs={'readonly': 'readonly'})
        # Set the widget for the 'fecha' field to read-only text input
        context['form'].fields['fecha'].widget = forms.TextInput(attrs={'readonly': 'readonly'})
        # Set the widget for the 'categoria' field to read-only text input
        context['form'].fields['categoria'].widget = forms.TextInput(attrs={'readonly': 'readonly'})
        context['title'] = 'Editar fuente'
        context['edit_msg'] = 'Los Campos Destino, Fecha y Categoria no pueden ser editados'    

        return context


class FuenteInfoDataturDelete(DeleteView):
    model = DataTour
    success_url = reverse_lazy('dashboard:fuente_info_datatour')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.delete()
        return HttpResponseRedirect(success_url)

@require_GET
def upload_file(request):
    if request.method == 'GET' and request.FILES['file']:
        file = request.FILES['file']
        if file.name.endswith('.csv'):
            data = pd.read_csv(file)
            # Process the CSV data and save it to the database
            # ...
        elif file.name.endswith('.xlsx'):
            data = pd.read_excel(file)
            # Process the Excel data and save it to the database
            # ...
        else:
            return HttpResponse('Invalid file type')
        return HttpResponse('File uploaded successfully')
    return HttpResponse('No file uploaded')