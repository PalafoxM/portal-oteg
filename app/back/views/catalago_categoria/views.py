
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.urls import reverse_lazy
from back.models import  *
from back.forms import *
from django.http import JsonResponse, HttpResponseRedirect
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


class CatalagoCategoriaListView(LoginRequiredMixin, SuperAdminMixin, ListView):
    model = CatalagoCategoria
    template_name = 'back/catalago_categoria/list.html'

    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Catalago Categorías'
        context['create_url'] = reverse_lazy('dashboard:catalago_categoria_create')
        context['entity'] = 'Catalago Categorías'
        context['d_route'] = 'Configuración  > Catalago Categorías' 
        return context


class  CatalagoCategoriaCreateView(LoginRequiredMixin, SuperAdminMixin, CreateView):
    model = CatalagoCategoria
    form_class = CatalagoCategoriaForm
    template_name = 'back/components/create_update.html'
    success_url = reverse_lazy('dashboard:catalago_categoria_list')

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
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
                'message': 'Ha ocurrido un error al crear un registro.',
                'errors': form.errors
            }
            return JsonResponse(data)
        

    def form_invalid(self, form):
        response = super().form_invalid(form)
        data = {
            'success': False,
            'message': 'Ha ocurrido un error al crear un registro.',
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
        context['title'] = 'Crear Registro'
        context['entity'] = 'Catalago Categorías'
        context['list_url'] = reverse_lazy('dashboard:catalago_categoria_list')
        context['action'] = 'add'
        context['d_route'] = 'Configuración  > Catalago Categorías' 
        return context


class CatalagoCategoriaUpdateView(LoginRequiredMixin, SuperAdminMixin,  UpdateView):
    model = CatalagoCategoria
    form_class = CatalagoCategoriaForm
    template_name = 'back/components/create_update.html'
    success_url = reverse_lazy('dashboard:catalago_categoria_list')

    def form_invalid(self, form):
        response = super().form_invalid(form)
        data = {
            'success': False,
            'message': 'Ha ocurrido un error al editar el registro.',
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
            'message': 'Registro creado exitosamente.',
            'url': self.success_url
        }
        if is_ajax(self.request):
            return JsonResponse(data)
        else:
            return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar Categoría'
        context['entity'] = 'Catalago Categoría'
        context['list_url'] = reverse_lazy('dashboard:catalago_categoria_list')
        context['form'] = self.form_class(instance=self.object)
        context['action'] = 'adit'
        context['d_route'] = 'Configuración  > Catalago Categorías' 
        return context


class CatalagoCategoriaDeleteView(LoginRequiredMixin, SuperAdminMixin, DeleteView):
    model = CatalagoCategoria
    # template_name = 'back/delete.html'
    success_url = reverse_lazy('dashboard:catalago_categoria_list')
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.delete()
        return HttpResponseRedirect(success_url)