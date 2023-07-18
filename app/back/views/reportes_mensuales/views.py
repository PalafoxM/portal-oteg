from django.shortcuts import render
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from back.models import *
from back.forms import *
from web.models import *
from django.contrib.auth.decorators import login_required, permission_required
from django.utils.decorators import method_decorator
from django.http import Http404
from django.core.exceptions import PermissionDenied
from back.mixins import *
from django.contrib.auth.decorators import user_passes_test

def es_admin_o_superadmin(user):
    return user.is_authenticated and (user.is_staff or user.is_superuser)


def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'


class ReporteMensualView (SuperAdminOrAdminMixin, LoginRequiredMixin, ListView):
    model = Reportes_Mensuales
    template_name = 'back/reportes_mensuales/viewer.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de  Boletines Mensuales'
        context['create_url'] =  reverse_lazy('dashboard:reporte_mensual_create')
        context['d_route'] = 'CEDOC > Boletines Mensuales'
        return context



class ReporteMensualCreate (SuperAdminOrAdminMixin, LoginRequiredMixin, CreateView):
    model = Reportes_Mensuales
    form_class = ReporteMensualForm
    template_name = 'back/components/create_update.html'

    success_url = reverse_lazy('dashboard:modulo_reportes_mensuales')

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST ,request.FILES)
        if form.is_valid():
            self.object = form.save()
            data = {
                'success': True,
                'message': 'Palabra Creada exitosamente.',
                'url': self.success_url
            }
            return JsonResponse(data)
        else:
            data = {
                'success': False,
                'message': 'Hubo un error al crear registro.',
                'errors': form.errors
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
        context['title'] = 'Crear Reporte Mensual'
        context['entity'] = 'Reporte Mensual'
        context['list_url'] = reverse_lazy('dashboard:modulo_reportes_mensuales')
        context['action'] = 'add'
        context['d_route'] = 'CEDOC > Boletines Mensuales'
        return context

    
class ReporteMensualUpdate (SuperAdminOrAdminMixin, LoginRequiredMixin, UpdateView):
    model = Reportes_Mensuales
    form_class = ReporteMensualForm
    template_name = 'back/components/create_update.html'
    success_url = reverse_lazy('dashboard:modulo_reportes_mensuales')

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
        context['form'] = self.form_class(instance=self.object)
        context['list_url'] = reverse_lazy('dashboard:modulo_reportes_mensuales')
        context['d_route'] = 'CEDOC > Boletines Mensuales'
        return context
    


class ReporteMensualDelete(SuperAdminOrAdminMixin, LoginRequiredMixin, DeleteView):

    model = Reportes_Mensuales
    success_url = reverse_lazy('dashboard:modulo_reportes_mensuales')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.delete()
        return HttpResponseRedirect(success_url)
    


class ReporteMensualDetail(ListView):
    model = Reportes_Mensuales
    template_name = 'back/reportes_mensuales/detail.html'

    def get_context_data(self, **kwargs):

        distinct_years = Reportes_Mensuales.objects.values('ano').distinct().order_by('ano')
    
        years_list = [item['ano'] for item in distinct_years]

        context = super().get_context_data(**kwargs)
        context['title'] = 'Detalle de Reporte Mensual'
        context['list_url'] = reverse_lazy('dashboard:modulo_reportes_mensuales')
        context['img_url'] = 'img_nav/publicaciones.jpg'
        context['nav_title'] = 'Boletines Mensuales'
        

        context['years'] = years_list
        
    
        return context