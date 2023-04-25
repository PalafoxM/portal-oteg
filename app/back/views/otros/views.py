from django.shortcuts import render, redirect, get_object_or_404
from back.models import *
from web.models import *

from back.forms import SeccionCentroDocumentalForm
from back.forms import CategoriasForm
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.views.decorators.http import require_GET


# Create your views here

def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'


class CentroDocumentalView(ListView):
    model = SeccionesCentroDocumental
    template_name = 'back/centro_documental/centro_documental.html'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado Secciones Centro Documental'
        context['create_url'] =  reverse_lazy('dashboard:centrodocumenta_create')
        return context
    
 
class SeccionCentroDocumentalDelete(DeleteView):
    model = SeccionesCentroDocumental
    success_url = reverse_lazy('dashboard:centrodocumental')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.delete()
        return HttpResponseRedirect(success_url)


class SeccionCentroDocumentalUpdate(UpdateView):
    model = SeccionesCentroDocumental
    form_class = SeccionCentroDocumentalForm
    template_name = 'back/components/create_update.html'
    success_url = reverse_lazy('dashboard:centrodocumental')

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
        context['list_url'] = reverse_lazy('dashboard:centrodocumental')
        return context

    
class SeccionCentroDocumentalCreate(CreateView):
    model = SeccionesCentroDocumental
    form_class = SeccionCentroDocumentalForm
    template_name = 'back/components/create_update.html'
    success_url = reverse_lazy('dashboard:centrodocumental')

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            self.object = form.save()
            data = {
                'success': True,
                'message': 'Evento creado exitosamente.',
                'url': self.success_url
            }
            return JsonResponse(data)
        else:
            data = {
                'success': False,
                'message': 'Hubo un error al crear el evento.',
                'errors': form.errors
            }
            return JsonResponse(data)

    def form_invalid(self, form):
        response = super().form_invalid(form)
        data = {
            'success': False,
            'message': 'Hubo un error al crear el evento.',
            'errors': form.errors
        }
        return JsonResponse(data)

    def form_valid(self, form):
        response = super().form_valid(form)
        data = {
            'success': True,
            'message': 'Evento creado exitosamente.',
            'url': self.success_url
        }
        return JsonResponse(data)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Crear una Seccion'
        context['entity'] = 'Secciones Centro Documental'
        context['list_url'] = reverse_lazy('dashboard:centrodocumental')
        context['action'] = 'add'
        return context
    

def edit_seccion(request, seccion_id):

    seccion = SeccionesCentroDocumental.objects.get(id=seccion_id)

    if request.method == 'POST':
        form = SeccionCentroDocumentalForm(request.POST, instance=seccion)
        if form.is_valid():
            form.save()
            return redirect('centrodocumental')
    else:
        form = SeccionCentroDocumentalForm(instance=seccion)

    return render(request, 'back/otros/otros/edit_seccion.html', {'form': form})


class CategoriasListView(ListView):
    model = Categorias
    template_name = 'back/centro_documental/categorias.html'
    context_object_name = 'categorias_list'
    paginate_by = 10

    def get_queryset(self):
        seccion_id = self.kwargs.get('pk')
        seccion = get_object_or_404(SeccionesCentroDocumental, pk=seccion_id)
        return Categorias.objects.filter(seccion=seccion)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        seccion_id = self.kwargs.get('pk')
        seccion = get_object_or_404(SeccionesCentroDocumental, pk=seccion_id)
        context['seccion'] = seccion
        context['is_category'] = True
        context['pk'] = seccion_id
        return context

class CategoriasCreateView(CreateView):
    model = Categorias
    form_class = CategoriasForm
    template_name = 'back/components/create_update.html'
    success_url = reverse_lazy('dashboard:categorias_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['pk'] = self.kwargs['pk']
        return kwargs

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            self.success_url = reverse_lazy('dashboard:categorias_list', kwargs={'pk': self.kwargs['pk']})
            self.object = form.save()
            data = {
                'success': True,
                'message': 'Categoria creada creado exitosamente.',
                'url': self.success_url
            }
            return JsonResponse(data)
        else:
            data = {
                'success': False,
                'message': 'Hubo un error al crear la categoria.',
                'errors': form.errors
            }
            return JsonResponse(data)

    def form_invalid(self, form):
        response = super().form_invalid(form)
        data = {
            'success': False,
            'message': 'Hubo un error al crear la categoria.',
            'errors': form.errors
        }
        return JsonResponse(data)

    def form_valid(self, form):
        response = super().form_valid(form)
        self.success_url = reverse_lazy('dashboard:categorias_list', kwargs={'pk': self.kwargs['pk']})
        data = {
            'success': True,
            'message': 'Categoria creada exitosamente.',
            'url': self.success_url
        }
        return JsonResponse(data)
    
    def get_context_data(self, **kwargs):
        
        context = super().get_context_data(**kwargs)
        context['title'] = 'Crear una Seccion'
        context['entity'] = 'Categoria'
        context['list_url'] = reverse_lazy('dashboard:categorias_list', kwargs={'pk': self.kwargs['pk']})
        context['action'] = 'add'
        return context

class CategoriasDeleteView(DeleteView):
    model = Categorias
    success_url = reverse_lazy('dashboard:centrodocumental')

    def get_success_url(self):
        seccion_pk = self.kwargs['seccion_pk']
        return reverse_lazy('dashboard:categorias_list', kwargs={'pk': seccion_pk})

class CategoriasUpdateView(UpdateView):
    model = Categorias
    form_class = CategoriasForm
    template_name = 'back/components/create_update.html'
    success_url =  reverse_lazy('dashboard:centrodocumental')

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
        self.success_url = reverse_lazy('dashboard:categorias_list', kwargs={'pk': self.kwargs['seccion_pk']})
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
        seccion_pk = self.kwargs['seccion_pk']
        context['list_url'] = reverse_lazy('dashboard:categorias_list', kwargs={'pk': seccion_pk})
        return context



def descargas_list(request):

    data = {
        'title': 'Listado de Banners',
        'descargas': [{'name': 'Listado de Boletín'},{'name': 'Listado de Colaboradores'}],
        'create_url': '#'
    }

    return render(request, 'back/descargas/list.html', data)

class DescargasView (ListView):

    template_name = 'back/descargas/viewer.html'
    context_object_name = 'descargas'
    paginate_by = 10

    def get_queryset(self):
        queryset1 = Publications.objects.all()
        queryset2 = BarometroTuristico.objects.all()
        queryset = list(queryset1) + list(queryset2)
        return queryset


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Descargas'
        return context      


@require_GET
def get_sections(request):
    q = request.GET.get('q', '')

    results = SeccionesCentroDocumental.objects.all()  

    data = [{'titulo': obj.seccion, 'id': obj.id } for obj in results]
    return JsonResponse(data, safe=False)
