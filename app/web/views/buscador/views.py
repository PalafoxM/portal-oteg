from django.views.generic import TemplateView, View
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from web.models import *
from back.models import *
from django.http import HttpResponse, StreamingHttpResponse
from django.core.signals import request_finished
from django.dispatch import receiver
from itertools import groupby
from operator import attrgetter
from django.db.models import F
import requests
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from back.models import Banner, Noticia
from datetime import datetime, timedelta
from django.http import Http404




# @require_GET
# def buscador_cedoc(request):
#     q = request.GET.get('q', '')
#     bim = request.GET.gt('bim', '')

#     results = Publications.objects.filter(name=q)

#     data = [{'nombrePDF': obj.nombrePDF, 'url': obj.doc.url, 'id': obj.id}
#             for obj in results]
#     return JsonResponse(data, safe=False)


from django.shortcuts import render

def search_view(request):

    query = request.GET.get('query')  # Retrieve the search query
    # Perform your search logic using the query
    queryset = Publications.objects.filter(name__icontains=query)

    publicaciones = queryset  # Assuming this is the object you want to iterate over


    # Pass the search results and properties to the template
    context = {
        'query': query,
        'publicaciones': publicaciones,
        'img_url' :'img_nav/barometro.jpg',
        'nav_title' : "Buscador CEDOC"
        # Include other relevant data for displaying search results
    }
    return render(request, 'web/search_results.html', context)