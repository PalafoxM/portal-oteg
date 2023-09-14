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


def search_destinos (request):

    query_original = request.GET.get('term', '')
    queryset = CatalagoDestino.objects.filter(destino__icontains=query_original)
    destinos = [ destino.destino for destino in queryset ]

    return JsonResponse(destinos, safe=False)


def search_categorias (request):

    query_original = request.GET.get('term', '')
    queryset = CatalagoCategoria.objects.filter(categoria__icontains=query_original)
    categorias = [ categoria.categoria for categoria in queryset ]

    return JsonResponse(categorias, safe=False)


def search_nombre_za (request):

    query_original = request.GET.get('term', '')
    queryset = CatalagoZAMuseos.objects.filter(nombre__icontains=query_original)
    nombres = [ nombre.nombre for nombre in queryset ]

    return JsonResponse(nombres, safe=False)

def search_entidades(request):
    
        query_original = request.GET.get('term', '')
        queryset = CatalogoEntidad.objects.filter(entidad__icontains=query_original)
        entidades = [ entidad.entidad for entidad in queryset ]
    
        return JsonResponse(entidades, safe=False)

def search_destino_aeropuerto (request):

    query_original = request.GET.get('term', '')
    queryset = CatalagoDestinoAeropuerto.objects.filter(destino_aeropuerto__icontains=query_original)
    destinos = [ destino.destino_aeropuerto for destino in queryset ]

    return JsonResponse(destinos, safe=False)


def search_id_destino_aeropuerto (request):

    id_destino_aeropuerto = request.GET.get('id_destino_aeropuerto')
    print(id_destino_aeropuerto)
    # Retrieve data from the model based on the value
    other_data = CatalagoDestinoAeropuerto.objects.filter(destino_aeropuerto=id_destino_aeropuerto).first()

    # Format the data as needed (e.g., extract a specific field)
    if other_data:
        other_data_value = other_data.destino_aeropuerto_id
    else:
        other_data_value = ''

    # Return the data as a JSON response
    return JsonResponse({'other_data_value': other_data_value})


def search_aeropuerto (request):

    query_original = request.GET.get('term', '')
    queryset = CatalogoAeropuertos.objects.filter(aereopuerto__icontains=query_original)
    
    destinos = [ destino.aereopuerto for destino in queryset ]

    return JsonResponse(destinos, safe=False)


def search_entidad_aeropuerto (request):

    id_entidad = request.GET.get('id_destino_aeropuerto')
    print(id_entidad)
    # Retrieve data from the model based on the value
    other_data = CatalogoAeropuertos.objects.filter(aereopuerto=id_entidad).first()

    # Format the data as needed (e.g., extract a specific field)
    if other_data:
        other_data_value = other_data.entidad
    else:

        other_data_value = ''

    # Return the data as a JSON response
    return JsonResponse({'other_data_value': other_data_value})


def search_categorias_eniot (request):

    query_original = request.GET.get('term', '')
    queryset = Categorias_Eniot.objects.filter(categoria__icontains=query_original)
    
    categorias = [ categorias.categoria for categorias in queryset ]

    return JsonResponse(categorias, safe=False)