from django.shortcuts import render, redirect
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from django.urls import reverse_lazy
from back.models import  *
from back.forms import *
from django.http import JsonResponse, HttpResponseRedirect

from django.views import View
from django.contrib import messages
from openpyxl import load_workbook
import csv
import os
import datetime



# Create your views here.
def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'
class InventarioHoteleroListView(ListView):
    model = InventarioHotelero
    template_name = 'back/estadisticas/list.html'

    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de inventario hotelero'
        context['create_url'] = reverse_lazy('dashboard:inventario_hotelero_create')
        context['carga_masiva_url'] = reverse_lazy('dashboard:inventario_hotelero_carga_masiva')
        context['entity'] = 'Inventario Hotelero'
        return context

class  InventarioHoteleroCreateView(CreateView):
    model = InventarioHotelero
    form_class = InventarioHoteleroForm
    template_name = 'back/components/create_update.html'
    success_url = reverse_lazy('dashboard:inventario_hotelero_list')

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            self.object = form.save()
            data = {
                'success': True,
                'message': 'Registro creado exitosamente.',
                'url': self.success_url
            }
            return JsonResponse(data)
        else:
            data = {
                'success': False,
                'message': 'Ha ocurrido un error al crear un registro.',
                'errors': form.errors
            }
            return JsonResponse(data)
        

    def form_invalid(self, form):
        response = super().form_invalid(form)
        data = {
            'success': False,
            'message': 'Ha ocurrido un error al crear un registro.',
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
        context['title'] = 'Crear Registro'
        context['entity'] = 'Inventario Hotelero'
        context['list_url'] = reverse_lazy('dashboard:inventario_hotelero_list')
        context['action'] = 'add'
        return context

class InventarioHoteleroUpdateView( UpdateView):
    model = InventarioHotelero
    form_class = InventarioHoteleroForm
    template_name = 'back/components/create_update.html'
    success_url = reverse_lazy('dashboard:inventario_hotelero_list')

    def form_invalid(self, form):
        response = super().form_invalid(form)
        data = {
            'success': False,
            'message': 'Ha ocurrido un error al editar el registro.',
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
            'message': 'Registro creado exitosamente.',
            'url': self.success_url
        }
        if is_ajax(self.request):
            return JsonResponse(data)
        else:
            return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar Inventario Hotelero'
        context['entity'] = 'Inventario Hotelero'
        context['list_url'] = reverse_lazy('dashboard:inventario_hotelero_list')
        context['form'] = self.form_class(instance=self.object)
        return context

class InventarioHoteleroDeleteView(DeleteView):
    model = InventarioHotelero
    # template_name = 'back/delete.html'
    success_url = reverse_lazy('dashboard:inventario_hotelero_list')
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.delete()
        return HttpResponseRedirect(success_url)

class CargaMasivaView(View):
    form_class = CargaMasivaForm
    template_name = 'back/estadisticas/carga_masiva.html'
    success_url = reverse_lazy('dashboard:inventario_hotelero_list')

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        registros_correctos = []
        registros_incorrectos = []
        if form.is_valid():
            archivo = request.FILES['archivo']
            extension = os.path.splitext(archivo.name)[1]
            if extension == '.xlsx':
                workbook = load_workbook(filename=archivo, read_only=True)
                worksheet = workbook.active
                filas = list(worksheet.rows)
                for i, row in enumerate(filas):
                    if i == 0:
                        continue # Ignorar la primera fila si es el encabezado
                    destino = row[0].value
                    fecha = row[1].value
                    categoria = row[2].value
                    habitaciones = row[3].value
                    establecimientos = row[4].value

                    # Aquí se crea una instancia del modelo correspondiente para cada fila en el archivo
                    # Se deben validar los datos y guardarlos en la base de datos
                    # Ejemplo:
                    try:
                        # Validar los datos
                        fecha_str = str(fecha)
                        fecha_obj = datetime.datetime.strptime(fecha_str, '%Y-%m-%d %H:%M:%S').date()
                        # fecha_obj = datetime.datetime.strptime(fecha, '%Y-%m-%d').date()
                        habitaciones_int = int(habitaciones)
                        establecimientos_int = int(establecimientos)
                        print(f"datos aceptados: {destino}, {fecha_obj}, {categoria}, {habitaciones_int}, {establecimientos_int}")
                        # Crear la instancia del modelo y guardarla en la base de datos
                        # Ejemplo:
                        inventario = InventarioHotelero(destino=destino, fecha=fecha_obj, categoria=categoria, habitaciones=habitaciones_int, establecimientos=establecimientos_int)
                        registros_correctos.append(inventario)
                        inventario.save()

                    except (ValueError, TypeError):
                        # Si ocurre un error al validar o guardar los datos, se ignora la fila
                        print(f"datos no aceptados: {destino}, {fecha}, {categoria}, {habitaciones}, {establecimientos}")
                        error = f"Datos no aceptados: {destino}, {fecha}, {categoria}, {habitaciones}, {establecimientos}. {str(e)}"
                        print(error)
                        registros_incorrectos.append(error)
                if len(registros_incorrectos) > 0:
                    messages.error(request, 'Hay errores de registros')
                    return render(request, self.template_name, {
                            'form': form,
                            'registros_correctos': registros_correctos,
                            'registros_incorrectos': registros_incorrectos,
                        })        

            elif extension == '.csv':
                datos = csv.DictReader(archivo.read().decode('latin-1').splitlines())
                for i, row in enumerate(datos):
                    destino = row['destino']
                    fecha = row['fecha']
                    categoria = row['categoria']
                    habitaciones = row['habitaciones']
                    establecimientos = row['establecimientos']

                    # Aquí se crea una instancia del modelo correspondiente para cada fila en el archivo
                    # Se deben validar los datos y guardarlos en la base de datos
                    # Ejemplo:
                    try:
                        # Validar los datos
                        fecha_str = str(fecha)
                        fecha_obj = datetime.datetime.strptime(fecha_str, '%d/%m/%Y').date()
                        habitaciones_int = int(habitaciones)
                        establecimientos_int = int(establecimientos)
                        # Crear la instancia del modelo y guardarla en la base de datos
                        # Ejemplo:
                        inventario = InventarioHotelero(destino=destino, fecha=fecha_obj, categoria=categoria, habitaciones=habitaciones_int, establecimientos=establecimientos_int)
                        registros_correctos.append(inventario.toJSON())
                        inventario.save()
                    except (ValueError, TypeError ):
                        # Si ocurre un error al validar o guardar los datos, se ignora la fila
                        print(f"datos no aceptados: {destino}, {fecha}, {categoria}, {habitaciones}, {establecimientos}")
                        error = f"Dato no aceptado: destino: {destino}, fecha: {fecha}, categoria: {categoria}, numero de habitaciones: {habitaciones}, numero de establecimientos{establecimientos}"
                        registros_incorrectos.append(error)
                        pass
                if len(registros_incorrectos) > 0:
                    messages.error(request, 'Hay errores de registros')
                    return render(request, self.template_name, {
                            'form': form,
                            'registros_correctos': registros_correctos,
                            'registros_incorrectos': registros_incorrectos,
                        })
            else:
                print("*paso 1")
                messages.error(request, 'El archivo debe ser un archivo .xlsx o .csv')
                registros_incorrectos.append("El archivo debe ser un archivo .xlsx o .csv")
                return render(request, self.template_name, {
                        'form': form,
                        'registros_correctos': registros_correctos,
                        'registros_incorrectos': registros_incorrectos,
                    })
            messages.success(request, 'El archivo se ha procesado correctamente')
            return redirect(self.success_url)
    
    