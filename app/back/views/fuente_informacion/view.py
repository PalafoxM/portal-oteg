from django.shortcuts import render, redirect, get_object_or_404
from back.models import *
from django.views.generic import ListView, TemplateView
from datetime import datetime, timedelta
from django.utils import timezone
from django.contrib.auth.decorators import login_required, permission_required
from django.utils.decorators import method_decorator
from django.http import Http404
from django.core.exceptions import PermissionDenied
from django.contrib.auth.mixins import *
from back.mixins import *

from django.contrib.auth.decorators import user_passes_test



class FuentesInfoView (SuperAdminOrAdminMixin, LoginRequiredMixin,  TemplateView):
    template_name = 'back/fuente-informacion/list.html'
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Fuentes de información'
        context['d_route'] = 'Fuentes de información > Dashboard'

        # model_updated = {}
        # total_registers = {}
        # last_updated = {}
        # non_updated_count = 0  # Variable to store the count of non-updated models

    
        # current_datetime = timezone.now()

        # #determinar si el modelo esta actualizado

        # #model1 
        # model1_last_updated_date = CalidadAire.objects.latest('fecha_actualizacion').fecha_actualizacion
        # model1_last_updated_datetime = datetime.combine(model1_last_updated_date, datetime.min.time())
        # #año en segundos
        # update_period = 2.628e+6  # define your desired update period in seconds

        # time_difference = current_datetime - model1_last_updated_datetime
        # model_updated['aire'] = time_difference.total_seconds() <= update_period


        # #model2

        # model2_last_updated_date = InventarioHoteleroEntNac.objects.latest('fecha_actualizacion').fecha_actualizacion
        # model2_last_updated_datetime = datetime.combine(model2_last_updated_date, datetime.min.time())
        # #mes en segundos
        # update_period = 2.628e+6  # define your desired update period in seconds
        # time_difference = current_datetime - model2_last_updated_datetime
        # model_updated['hotelero_nac'] = time_difference.total_seconds() <= update_period

        # #model3

        # model3_last_updated_date = Airbnb.objects.latest('fecha_actualizacion').fecha_actualizacion
        # model3_last_updated_datetime = datetime.combine(model3_last_updated_date, datetime.min.time())
        # #mes en segundos
        # update_period = 2.628e+6  # define your desired update period in seconds
        # time_difference = current_datetime - model3_last_updated_datetime
        # model_updated['airbnb'] = time_difference.total_seconds() <= update_period




        # #model 4
        # model4_last_updated_date = Certificacion.objects.latest('fecha_actualizacion').fecha_actualizacion
        # model4_last_updated_datetime = datetime.combine(model4_last_updated_date, datetime.min.time())

        # #mes en segundos
        # update_period = 2.628e+6  # define your desired update period in seconds
        # time_difference = current_datetime - model4_last_updated_datetime
        # model_updated['certificacion'] = time_difference.total_seconds() <= update_period




        # #count the updated models
        # if not model_updated['aire']:
        #     non_updated_count += 1

        # if not model_updated['hotelero_nac']:
        #     non_updated_count += 1
        
        # if not model_updated['airbnb']:
        #     non_updated_count += 1
        
        # if not model_updated['certificacion']:
        #     non_updated_count += 1


        # #register count
        # total_registers['aire'] = CalidadAire.objects.all().count()

        # total_registers['hotelero_nac'] = InventarioHoteleroEntNac.objects.all().count()

        # total_registers['airbnb'] = Airbnb.objects.all().count()

        # total_registers['certificacion'] = Certificacion.objects.all().count()




        # #last updated
        # last_updated['aire'] = CalidadAire.objects.latest('fecha_actualizacion').fecha_actualizacion
        # last_updated['hotelero_nac'] = InventarioHoteleroEntNac.objects.latest('fecha_actualizacion').fecha_actualizacion
        # last_updated['airbnb'] = Airbnb.objects.latest('fecha_actualizacion').fecha_actualizacion




        # context['model_updated'] = model_updated
        # context['total_registers'] = total_registers
        # context['non_updated_count'] = non_updated_count
        # context['last_updated'] = last_updated
        # context['totla_F_updated'] = 38-non_updated_count


        model_info = [
        {
            'model': CalidadAire,
            'key': 'aire',
            'update_period': 2.628e+6  # define your desired update period in seconds
        },
        {
            'model': InventarioHoteleroEntNac,
            'key': 'hotelero_nac',
            'update_period': 2.628e+6
        },
        {
            'model': Airbnb,
            'key': 'airbnb',
            'update_period': 2.628e+6
        },
        {
            'model': Certificacion,
            'key': 'certificacion',
            'update_period': 3.154e+7
        },
        {
            'model': DataTour,
            'key': 'datatur',
            'update_period': 2.628e+6
        },
        {
            'model': empleo,
            'key': 'empleo',
            'update_period':7.884e+6

        },
        {
            'model': Discapacidad,
            'key': 'discapacidad',
            'update_period': 2.628e+6 
        },
        {
            'model': GastoDerrama,
            'key': 'gasto_derrama',
            'update_period': 3.154e+7 #año
        },
        {
            'model': InventarioHotelero,
            'key': 'hotelero_gto',
            'update_period': 2.628e+6 #mes
        },
        {
            'model': inversion_privada,
            'key': 'inversion_privada',
            'update_period': 2.628e+6 #mes
        },
        {
            'model': InversionPublica,
            'key': 'inversion_publica',
            'update_period': 3.154e+7 #año
        }, 
        {
            'model': otros_anuales,
            'key': 'otros_anuales',
            'update_period': 3.154e+7 #año
        },
        {
            'model': Sensivilizacion,
            'key': 'sensibilizacion',
            'update_period': 3.154e+7 #año
        },{
            'model': zonas_arqueologicas_museos,
            'key': 'zonas_arqueologicas',
            'update_period':  2.628e+6 #mes
        },{
            'model': Aerolinea,
            'key': 'aerolinea',
            'update_period':  2.628e+6 #mes
        },{
            'model': FuenteInfoEntornoN,
            'key': 'entorno_n',
            'update_period': 3.154e+7 #año
        },{
            'model': Aeropuerto,
            'key': 'aeropuerto',
            'update_period': 2.628e+6 #mes
        },{
            'model': ParticipacionOrigen,
            'key': 'participacion_origen',
            'update_period': 2.628e+6 #mes

        },{

            'model': ParticipacionSegmentos,
            'key': 'participacion_segmentos',
            'update_period': 2.628e+6 #mes
        },{
            'model': ProyectoInversion,
            'key': 'proyecto_inversion',
            'update_period':3.154e+7 #año
        }

        ]

        model_updated = {}
        total_registers = {}
        last_updated = {}
        non_updated_count = 0

        current_datetime = timezone.now()

        for info in model_info:
            model = info['model']
            key = info['key']
            update_period = info['update_period']

            last_updated_date = model.objects.latest('fecha_actualizacion').fecha_actualizacion
            last_updated_datetime = datetime.combine(last_updated_date, datetime.min.time())

            time_difference = current_datetime - last_updated_datetime
            model_updated[key] = time_difference.total_seconds() <= update_period

            if not model_updated[key]:
                non_updated_count += 1

            total_registers[key] = model.objects.all().count()
            last_updated[key] = last_updated_date

        context['model_updated'] = model_updated
        context['total_registers'] = total_registers
        context['non_updated_count'] = non_updated_count
        context['last_updated'] = last_updated
        context['total_F_updated'] = 39 - non_updated_count

        user_in_colaboradores_group = self.request.user.groups.filter(name='colaboradores').exists()
        # context['user_in_colaboradores_group'] = user_in_colaboradores_group

        return context