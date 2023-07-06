from django.shortcuts import render, redirect, get_object_or_404
from back.models import *
from django.views.generic import ListView, TemplateView
from datetime import datetime, timedelta
from django.utils import timezone
from django.contrib.auth.decorators import login_required, permission_required
from django.utils.decorators import method_decorator
from django.http import Http404
from django.core.exceptions import PermissionDenied

from django.contrib.auth.decorators import user_passes_test

def es_admin_o_superadmin(user):
    return user.is_authenticated and (user.is_staff or user.is_superuser)

@method_decorator(login_required(login_url='/auth/login_user'), name='dispatch')
@method_decorator(permission_required('auth.view_banner', raise_exception=True), name='dispatch')
@method_decorator(user_passes_test(es_admin_o_superadmin, login_url='404'), name='dispatch')
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

        user_in_colaboradores_group = self.request.user.groups.filter(name='colaboradores').exists()
        # context['user_in_colaboradores_group'] = user_in_colaboradores_group

        return context