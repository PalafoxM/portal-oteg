from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.shortcuts import render
from back.models import *
from back.forms import PublicationForm
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
#onjet of 404
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from django.contrib.auth.decorators import login_required, permission_required
from django.utils.decorators import method_decorator
from django.http import Http404
from django.core.exceptions import PermissionDenied
from back.mixins import *
from django.contrib.auth.decorators import user_passes_test

def es_admin_o_superadmin(user):
    return user.is_authenticated and ( user.is_staff or user.is_superuser)


# Create your views here.

class PublicationsListView(LoginRequiredMixin, SuperAdminMixin, ListView):

    model = Publications
    template_name = 'back/publicaciones/viewer.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Publicaciones'
        context['create_url'] =  reverse_lazy('dashboard:publicacion_create')
        return context
    


class PublicationsCreateView(LoginRequiredMixin, SuperAdminMixin, CreateView):
    model = Publications
    form_class = PublicationForm
    template_name = 'back/components/create_update_dynamic.html'
    success_url = reverse_lazy('dashboard:publicacion_list')
    
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST ,request.FILES) 

        if form.is_valid():
            section_id = request.POST.get('section')
            category_id = request.POST.get('category')
            section = SeccionesCentroDocumental.objects.get(pk=section_id)
            category = Categorias.objects.get(pk=category_id)
            
            # Set the section and category on the Publication object
            publication = form.save(commit=False)
            publication.section = section
            publication.category = category
            publication.save()

            #self.object = form.save()
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
        context['title'] = 'Crear una Publicacion'
        context['entity'] = 'Publicaciones'
        context['sections'] = SeccionesCentroDocumental.objects.all()
        context['list_url'] = reverse_lazy('dashboard:publicacion_list')
        context['action'] = 'add'
        return context


def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'



class PublicationUpdateView(LoginRequiredMixin, SuperAdminMixin, UpdateView):
    model = Publications
    form_class = PublicationForm
    template_name = 'back/components/update_dynamic.html'
    success_url = reverse_lazy('dashboard:publicacion_list')


    def form_invalid(self, form):
        response = super().form_invalid(form)
        data = {
            'success': False,
            'message': 'Hubo un error al crear la publicacion.',
            'errors': form.errors
        }
        if is_ajax(self.request):
            return JsonResponse(data)
        else:
            return response

    def form_valid(self, form):
        response = super().form_valid(form)
        section_id = self.request.POST.get('section')
        category_id = self.request.POST.get('category')
        section = SeccionesCentroDocumental.objects.get(pk=section_id)
        category = Categorias.objects.get(pk=category_id)
        
        # Set the section and category on the Publication object
        publication = form.save(commit=False)
        publication.section = section
        publication.category = category
        publication.save()



        data = {
            'success': True,
            'message': 'Publicacion creada exitosamente.',
            'url': self.success_url
        }
        if is_ajax(self.request):
            return JsonResponse(data)
        else:
            return response
        
        
    def get_object(self):
        # Get the Publicacion object to update based on the pk value from the URL
        pk = self.kwargs.get('pk')
        return Publications.objects.get(pk=pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sections'] = SeccionesCentroDocumental.objects.all()
        context['form'] = self.form_class(instance=self.object)
        context['list_url'] = reverse_lazy('dashboard:publicacion_list')
        context ['pk'] = self.kwargs.get('pk')
        context ['section'] = self.object.section.id
        context ['category'] = self.object.category.id
        return context


class PublicationDeleteView(LoginRequiredMixin, SuperAdminMixin, DeleteView):
    model = Publications
    success_url = reverse_lazy('dashboard:publicacion_list')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.delete()
        return HttpResponseRedirect(success_url)
    
@require_GET
def get_categories(request):
    section_id = request.GET.get('section_id', 0)

    if section_id:
        seccion = get_object_or_404(SeccionesCentroDocumental, id=section_id)

        categories = Categorias.objects.filter(seccion=seccion)


    data = [{'key': c.id, 'value': c.nombre_categoria} for c in categories]

    return JsonResponse(data, safe=False)
