
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.urls import reverse_lazy
from back.models import  *
from back.forms import *
from django.http import JsonResponse, HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
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


class ProyectoInversionListView(SuperAdminOrAdminMixin, LoginRequiredMixin, ListView):
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


class  ProyectoInversionCreateView(SuperAdminOrAdminMixin, LoginRequiredMixin, CreateView):
    model = ProyectoInversion
    form_class = ProyectoInversionForm
    template_name = 'back/proyectos_inversion/create.html'
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


class ProyectoInversionUpdateView(SuperAdminOrAdminMixin, LoginRequiredMixin,  UpdateView):
    model = ProyectoInversion
    form_class = ProyectoInversionForm
    template_name = 'back/proyectos_inversion/view_editor.html'
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
        destino_widget = context['form'].fields['destino'].widget
        destino_widget.attrs.update({'readonly': 'readonly'})
        fecha_widget = context['form'].fields['nombre_del_proyecto'].widget
        fecha_widget.attrs.update({'readonly': 'readonly'})
        context['edit_msg'] = 'Los Campos que no se pueden editar están sombreados'
        return context


class ProyectoInversionDeleteView(SuperAdminOrAdminMixin, LoginRequiredMixin, DeleteView):
    model = ProyectoInversion
    # template_name = 'back/delete.html'
    success_url = reverse_lazy('dashboard:proyectos_inversion_list')
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        try:
            self.object.delete()
            return JsonResponse({'message': 'Eliminación exitosa.'})
        except Exception as e:
            return JsonResponse({'error': 'Error al eliminar el registro.'}, status=500)