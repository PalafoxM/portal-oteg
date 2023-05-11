
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.urls import reverse_lazy
from back.models import  *
from back.forms import *
from django.http import JsonResponse, HttpResponseRedirect




# Create your views here.
def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

class CatalagoTipoVisistanteListView(ListView):
    model = CatalagoTipoVisistante
    template_name = 'back/catalago_tipo_visitante/list.html'

    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Catalago Tipo de Visitante'
        context['create_url'] = reverse_lazy('dashboard:catalago_tipo_visitante_create')
        context['entity'] = 'Catalago Tipo de Visitante'
        return context

class  CatalagoTipoVisistanteCreateView(CreateView):
    model = CatalagoTipoVisistante
    form_class = CatalagoTipoVisistanteForm
    template_name = 'back/components/create_update.html'
    success_url = reverse_lazy('dashboard:catalago_tipo_visitante_list')

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
        context['entity'] = 'Catalago Tipo de Visitante'
        context['list_url'] = reverse_lazy('dashboard:catalago_tipo_visitante_list')
        context['action'] = 'add'
        return context

class CatalagoTipoVisistanteUpdateView( UpdateView):
    model = CatalagoTipoVisistante
    form_class = CatalagoTipoVisistanteForm
    template_name = 'back/components/create_update.html'
    success_url = reverse_lazy('dashboard:catalago_tipo_visitante_list')

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
        context['title'] = 'Editar Tipo de Visitante'
        context['entity'] = 'Catalago Tipo de Visitante'
        context['list_url'] = reverse_lazy('dashboard:catalago_tipo_visitante_list')
        context['form'] = self.form_class(instance=self.object)
        context['action'] = 'adit'
        return context

class CatalagoTipoVisistanteDeleteView(DeleteView):
    model = CatalagoTipoVisistante
    # template_name = 'back/delete.html'
    success_url = reverse_lazy('dashboard:catalago_tipo_visitante_list')
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.delete()
        return HttpResponseRedirect(success_url)