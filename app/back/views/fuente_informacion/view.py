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
        total_registers = {}
        last_updated = {}
        non_updated_count = 0  # Variable to store the count of non-updated models

    
        current_datetime = timezone.now()

        #determinar si el modelo esta actualizado

        #model1 
        model1_last_updated_date = CalidadAire.objects.latest('fecha_actualizacion').fecha_actualizacion
        model1_last_updated_datetime = datetime.combine(model1_last_updated_date, datetime.min.time())
        #año en segundos
        update_period = 2.628e+6  # define your desired update period in seconds

        time_difference = current_datetime - model1_last_updated_datetime
        model_updated['aire'] = time_difference.total_seconds() <= update_period


        #model2

        model2_last_updated_date = InventarioHoteleroEntNac.objects.latest('fecha_actualizacion').fecha_actualizacion
        model2_last_updated_datetime = datetime.combine(model2_last_updated_date, datetime.min.time())
        #mes en segundos
        update_period = 2.628e+6  # define your desired update period in seconds
        model_updated['hotelero_nac'] = time_difference.total_seconds() <= update_period

        #model3
        
        # model3_last_updated_date = InventarioHotelero.objects.latest('fecha_actualizacion').fecha_actualizacion
        # model3_last_updated_datetime = datetime.combine(model3_last_updated_date, datetime.min.time())

        # #mes en segundos
        # update_period = 2.628e+6  # define your desired update period in seconds



        #count the updated models
        if not model_updated['aire']:
            non_updated_count += 1

        if not model_updated['hotelero_nac']:
            non_updated_count += 1



        #register count
        total_registers['aire'] = CalidadAire.objects.all().count()

        total_registers['hotelero_nac'] = InventarioHoteleroEntNac.objects.all().count()


        #last updated
        last_updated['aire'] = CalidadAire.objects.latest('fecha_actualizacion').fecha_actualizacion
        last_updated['hotelero_nac'] = InventarioHoteleroEntNac.objects.latest('fecha_actualizacion').fecha_actualizacion

        context['model_updated'] = model_updated
        context['total_registers'] = total_registers
        context['non_updated_count'] = non_updated_count
        context['last_updated'] = last_updated
        context['totla_F_updated'] = 38-non_updated_count

        return context