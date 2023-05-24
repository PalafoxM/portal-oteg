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