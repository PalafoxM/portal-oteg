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


class EncuestaView(SuperAdminOrAdminMixin, LoginRequiredMixin, ListView):
    model = Encuesta
    template_name = 'back/modulo_encuestas/viewer.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado encuenstas'
        context['create_url'] = reverse_lazy('dashboard:encuesta_create')
        context['d_route'] = 'CEDOC > Encuestas'
        return context



class EncuestaCreate (CreateView):
    model = Encuesta
    form_class = EncuestaFormB
    template_name = 'back/components/create_update.html'
    success_url = reverse_lazy('dashboard:modulo_encuestas')

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
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
        context['title'] = 'Crear una Palabra'
        context['entity'] = 'Glosario'
        context['list_url'] = reverse_lazy('dashboard:modulo_encuestas')
        context['action'] = 'add'
        context['d_route'] = 'CEDOC > Encuestas'
        return context


class EncuestaUpdate (UpdateView):
    model = Encuesta
    form_class = EncuestaFormB
    template_name = 'back/components/create_update.html'
    success_url = reverse_lazy('dashboard:modulo_encuestas')
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
        context['list_url'] = reverse_lazy('dashboard:modulo_encuestas')
        context['d_route'] = 'CEDOC > Encuestas'
        return context


class EncuestaDelete (DeleteView):
    model = Encuesta
    # template_name = 'back/delete.html'
    success_url = reverse_lazy('dashboard:modulo_encuestas')
    

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        try:
            self.object.delete()
            return JsonResponse({'message': 'Eliminación exitosa.'})
        except Exception as e:
            return JsonResponse({'error': 'Error al eliminar el registro.'}, status=500)
