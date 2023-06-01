
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.urls import reverse_lazy
from back.models import  *
from back.forms import *
from django.http import JsonResponse, HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt




# Create your views here.
def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

class ProyectoInversionListView(ListView):
    model = ProyectoInversion
    template_name = 'back/proyectos_inversion/list.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs) :
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search':
                data = []
                for i in ProyectoInversion.objects.all():
                    data.append(i.toJSON())
            else:
                data.append({'error': 'Ha ocurrido un error'})
        except Exception as e:
            data.append({'error': str(e)})
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Proyectos privados'
        context['create_url'] = reverse_lazy('dashboard:proyectos_inversion_create')
        context['entity'] = 'Proyectos privados'
        return context

class  ProyectoInversionCreateView(CreateView):
    model = ProyectoInversion
    form_class = ProyectoInversionForm
    template_name = 'back/components/create_update.html'
    success_url = reverse_lazy('dashboard:proyectos_inversion_list')

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
        context['entity'] = 'Proyectos privados'
        context['list_url'] = reverse_lazy('dashboard:proyectos_inversion_list')
        context['action'] = 'add'
        return context

class ProyectoInversionUpdateView( UpdateView):
    model = ProyectoInversion
    form_class = ProyectoInversionForm
    template_name = 'back/components/create_update.html'
    success_url = reverse_lazy('dashboard:proyectos_inversion_list')

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
        context['list_url'] = reverse_lazy('dashboard:proyectos_inversion_list')
        context['form'] = self.form_class(instance=self.object)
        context['action'] = 'adit'
        return context

class ProyectoInversionDeleteView(DeleteView):
    model = ProyectoInversion
    # template_name = 'back/delete.html'
    success_url = reverse_lazy('dashboard:proyectos_inversion_list')
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.delete()
        return HttpResponseRedirect(success_url)