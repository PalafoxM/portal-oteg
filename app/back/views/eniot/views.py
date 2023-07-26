from django.shortcuts import render
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse_lazy , reverse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from back.models import  *
from back.forms import *
from django.contrib.auth.decorators import login_required, permission_required
from django.utils.decorators import method_decorator
from django.http import Http404
from django.core.exceptions import PermissionDenied
from back.mixins import *
from django.contrib.auth.decorators import user_passes_test

def es_admin_o_superadmin(user):
    return user.is_authenticated and (user.is_staff or user.is_superuser)


# Create your views here.
def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'


class EniotListView(SuperAdminOrAdminMixin, LoginRequiredMixin, ListView):
    model = Eniot
    template_name = 'back/eniot/viewer.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Eniot'
        context['create_url'] =  reverse_lazy('dashboard:eniot_create')
        context['d_route'] = 'Eniot'
        return context

        
class EniotCreateView(SuperAdminOrAdminMixin, LoginRequiredMixin, CreateView):
    model = Eniot
    form_class = EniotForm
    template_name = 'back/components/create_update.html'
    success_url = reverse_lazy('dashboard:eniot_list')
    
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)  # Incluir request.FILES para manejar los archivos subidos
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
        context['title'] = 'Crear Registro Eniot'
        context['entity'] = 'Eniot'
        context['list_url'] = reverse_lazy('dashboard:eniot_list')
        context['action'] = 'add'
        context['d_route'] = 'Eniot'
        return context

    
class EniotDeleteView(SuperAdminOrAdminMixin, LoginRequiredMixin, DeleteView):
    model = Eniot
    success_url = reverse_lazy('dashboard:eniot_list')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        try:
            self.object.delete()
            return JsonResponse({'message': 'Eliminación exitosa.'})
        except Exception as e:
            return JsonResponse({'error': 'Error al eliminar el registro.'}, status=500)


class EniotUpdateView(SuperAdminOrAdminMixin, LoginRequiredMixin, UpdateView):
    model = Eniot
    form_class = EniotForm
    template_name = 'back/components/create_update.html'
    success_url = reverse_lazy('dashboard:eniot_list')

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
        context['title'] = 'Actualizar Registro Eniot'
        context['form'] = self.form_class(instance=self.object)
        context['list_url'] = reverse_lazy('dashboard:eniot_list')
        context['d_route'] = 'Eniot'
        return context

    
class EniotAlbunListView(SuperAdminOrAdminMixin, LoginRequiredMixin, ListView):
    model = EniotAlbun
    template_name = 'back/eniot/foto_viewer.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'LISTADO ÁLBUMES'
        context['create_url'] =  reverse_lazy('dashboard:eniot_fotos_create')
        context['d_route'] = 'Eniot > Álbum'
        return context

        
class EniotAlbunCreateView(SuperAdminOrAdminMixin, LoginRequiredMixin, CreateView):
    model = EniotAlbun
    form_class = EniotAlbunForm
    template_name = 'back/components/create_update.html'
    success_url = reverse_lazy('dashboard:eniot_fotos_list')
    
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)  # Incluir request.FILES para manejar los archivos subidos
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
        context['title'] = 'Crear Registro EniotAlbun'
        context['entity'] = 'EniotAlbun'
        context['list_url'] = reverse_lazy('dashboard:eniot_fotos_list')
        context['action'] = 'add'
        context['d_route'] = 'Eniot > Álbum'
        return context

    
class EniotAlbunDeleteView(SuperAdminOrAdminMixin, LoginRequiredMixin, DeleteView):
    model = EniotAlbun
    success_url = reverse_lazy('dashboard:eniot_fotos_list')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        try:
            self.object.delete()
            return JsonResponse({'message': 'Eliminación exitosa.'})
        except Exception as e:
            return JsonResponse({'error': 'Error al eliminar el registro.'}, status=500)


class EniotAlbunUpdateView(SuperAdminOrAdminMixin, LoginRequiredMixin, UpdateView):
    model = EniotAlbun
    form_class = EniotAlbunForm
    template_name = 'back/components/create_update.html'
    success_url = reverse_lazy('dashboard:eniot_fotos_list')

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
        context['title'] = 'Actualizar Registro EniotAlbun'
        context['form'] = self.form_class(instance=self.object)
        context['list_url'] = reverse_lazy('dashboard:eniot_fotos_list')
        context['d_route'] = 'Eniot > Álbum'
        return context