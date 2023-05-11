
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.urls import reverse_lazy
from back.models import  *
from back.forms import *
from django.http import JsonResponse, HttpResponseRedirect




# Create your views here.
def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

class CatalagoSegmentosListView(ListView):
    model = CatalagoSegmentos
    template_name = 'back/catalago_segmento/list.html'

    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Catalago Segmentos'
        context['create_url'] = reverse_lazy('dashboard:catalago_segmento_create')
        context['entity'] = 'Catalago Segmentos'
        return context

class  CatalagoSegmentosCreateView(CreateView):
    model = CatalagoSegmentos
    form_class = CatalagoSegmentosForm
    template_name = 'back/components/create_update.html'
    success_url = reverse_lazy('dashboard:catalago_segmento_list')

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
        context['entity'] = 'Catalago Segmentos'
        context['list_url'] = reverse_lazy('dashboard:catalago_segmento_list')
        context['action'] = 'add'
        return context

class CatalagoSegmentosUpdateView( UpdateView):
    model = CatalagoSegmentos
    form_class = CatalagoSegmentosForm
    template_name = 'back/components/create_update.html'
    success_url = reverse_lazy('dashboard:catalago_segmento_list')

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
        context['title'] = 'Editar Segmentos'
        context['entity'] = 'Catalago Segmentos'
        context['list_url'] = reverse_lazy('dashboard:catalago_segmento_list')
        context['form'] = self.form_class(instance=self.object)
        context['action'] = 'adit'
        return context

class CatalagoSegmentosDeleteView(DeleteView):
    model = CatalagoSegmentos
    # template_name = 'back/delete.html'
    success_url = reverse_lazy('dashboard:catalago_segmento_list')
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.delete()
        return HttpResponseRedirect(success_url)