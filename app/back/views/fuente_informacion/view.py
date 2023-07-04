from django.shortcuts import render, redirect, get_object_or_404
from back.models import *
from django.views.generic import ListView, TemplateView
from datetime import datetime, timedelta
from django.utils import timezone

class FuentesInfoView (TemplateView):
    template_name = 'back/fuente-informacion/list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Fuentes de información'
        context['d_route'] = 'Fuentes de información > Dashboard'

        model_updated = {}
        non_updated_count = 0  # Variable to store the count of non-updated models

        # Check if each model has been updated within the specified time period
        # Adjust the timedelta according to the desired update period for each model
        # Repeat the following block for each of your models
        # update_period = timedelta(days=1)  # Example: Update period of 7 days
        # model1_last_updated = InventarioHotelero.objects.latest('updated_at').updated_at
        # model_updated['InventarioHotelero'] = timezone.now() - model1_last_updated <= update_period
        # if not model_updated['Model1']:
        #     non_updated_count += 1

        # model2_last_updated = InventarioHoteleroEntNac.objects.latest('updated_at').updated_at
        # model_updated['InventarioHoteleroEntNac'] = timezone.now() - model2_last_updated <= update_period
        # if not model_updated['Model2']:
        #     non_updated_count += 1

        # # Repeat the above two lines for each of your models

        # context['model_updated'] = model_updated
        # context['non_updated_count'] = non_updated_count

        return context