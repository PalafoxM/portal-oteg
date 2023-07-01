from django.shortcuts import render
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse_lazy , reverse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from back.models import  *
from back.forms import *


# Create your views here.
def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

class EniotListView(ListView):
    model = Eniot
    template_name = 'back/eniot/viewer.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado ENIOT'
        context['create_url'] =  reverse_lazy('dashboard:eniot_create')
        return context
        
class EniotCreateView(CreateView):
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
        return context
    
class EniotDeleteView(DeleteView):
    model = Eniot
    success_url = reverse_lazy('dashboard:eniot_list')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.delete()
        return HttpResponseRedirect(success_url)

class EniotUpdateView(UpdateView):
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
        context['form'] = self.form_class(instance=self.object)
        context['list_url'] = reverse_lazy('dashboard:eniot_list')
        return context
    
class EniotAlbunListView(ListView):
    model = EniotAlbun
    template_name = 'back/eniot/foto_viewer.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado ENIOT-fotos'
        context['create_url'] =  reverse_lazy('dashboard:eniot_fotos_create')
        return context
        
class EniotAlbunCreateView(CreateView):
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
        return context
    
class EniotAlbunDeleteView(DeleteView):
    model = EniotAlbun
    success_url = reverse_lazy('dashboard:eniot_fotos_list')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.delete()
        return HttpResponseRedirect(success_url)

class EniotAlbunUpdateView(UpdateView):
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
        context['form'] = self.form_class(instance=self.object)
        context['list_url'] = reverse_lazy('dashboard:eniot_fotos_list')
        return context