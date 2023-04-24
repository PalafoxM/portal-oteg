from django.shortcuts import render
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse_lazy , reverse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from back.models import  *
from back.forms import *


# Create your views here.
class BannerListView(ListView):
    model = Banner
    template_name = 'back/banner/list.html'

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search':
                data = []
                for i in PlacesOfInterest.objects.all():
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de banners'
        context['create_url'] = reverse_lazy('dashboard:banner_create')
        context['entity'] = 'Categorias'
        context['dropped_sidebar '] = False
        context['dropped '] = False
        context['moduleActive '] = 'Estadisticas'
        context['list'] = '2'
        context['subModuleActive '] = 'funtes-informacion'
        return context

class  BannerCreateView(CreateView):
    model = Banner
    form_class = BannerForm
    template_name = 'back/components/create_update.html'
    success_url = reverse_lazy('dashboard:banner_list')

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            self.object = form.save()
            data = {
                'success': True,
                'message': 'Banner creado exitosamente.',
                'url': self.success_url
            }
            return JsonResponse(data)
        else:
            data = {
                'success': False,
                'message': 'Hubo un error al crear un Banner.',
                'errors': form.errors
            }
            return JsonResponse(data)
        

    def form_invalid(self, form):
        response = super().form_invalid(form)
        data = {
            'success': False,
            'message': 'Hubo un error al crear un Banner.',
            'errors': form.errors
        }
        return JsonResponse(data)

    def form_valid(self, form):
        response = super().form_valid(form)
        data = {
            'success': True,
            'message': 'Banner creado exitosamente.',
            'url': self.success_url
        }
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Crear Banner'
        context['entity'] = 'Banners'
        context['list_url'] = reverse_lazy('dashboard:banner_list')
        context['action'] = 'add'
        return context

class BannerUpdateView( UpdateView):
    model = Banner
    form_class = BannerForm
    template_name = 'back/components/create_update.html'
    success_url = reverse_lazy('dashboard:banner_list')

    def form_invalid(self, form):
        response = super().form_invalid(form)
        data = {
            'success': False,
            'message': 'Hubo un error al crear el Banner.',
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
            'message': 'Banner creado exitosamente.',
            'url': self.success_url
        }
        if is_ajax(self.request):
            return JsonResponse(data)
        else:
            return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edición una Pulicacion'
        context['entity'] = 'Banners'
        context['list_url'] = reverse_lazy('dashboard:banner_list')
        context['form'] = self.form_class(instance=self.object)
        return context

class BanneDeleteView(DeleteView):
    model = Banner
    # template_name = 'back/delete.html'
    success_url = reverse_lazy('dashboard:banner_list')
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.delete()
        return HttpResponseRedirect(success_url)

class PlaceListView(ListView):
    model = PlacesOfInterest
    template_name = 'back/places_of_interest/list.html'
    
    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search':
                data = []
                for i in PlacesOfInterest.objects.all():
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Sitios de interes'
        context['create_url'] = reverse_lazy('dashboard:place_create')
        context['entity'] = 'Categorias'

        return context

class  PlaceCreateView(CreateView):
    model = PlacesOfInterest
    form_class = PlacesOfInterestForm
    template_name = 'back/components/create_update.html' 
    success_url = reverse_lazy('dashboard:place_list')

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            self.object = form.save()
            data = {
                'success': True,
                'message': 'Sitio de Interest creado exitosamente.',
                'url': self.success_url
            }
            return JsonResponse(data)
        else:
            data = {
                'success': False,
                'message': 'Hubo un error al crear un Sitio de Interest.',
                'errors': form.errors
            }
            return JsonResponse(data)
        

    def form_invalid(self, form):
        print("form_invalid")
        response = super().form_invalid(form)
        data = {
            'success': False,
            'message': 'Hubo un error al crear un Sitio de Interest.',
            'errors': form.errors
        }
        return JsonResponse(data)

    def form_valid(self, form):
        print("form_valid")
        response = super().form_valid(form)
        data = {
            'success': True,
            'message': 'Sitio de Interest creado exitosamente.',
            'url': self.success_url
        }
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Crear un Sitio de Interest'
        context['entity'] = 'Sitio de Interes'
        context['list_url'] = reverse_lazy('dashboard:place_list')
        return context

class PlaceUpdateView( UpdateView):
    model = PlacesOfInterest
    form_class = PlacesOfInterestForm
    template_name = 'back/components/create_update.html'
    success_url = reverse_lazy('dashboard:place_list')

    def form_invalid(self, form):
        response = super().form_invalid(form)
        data = {
            'success': False,
            'message': 'Hubo un error al crear el Sitio de Interest.',
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
            'message': 'Sitio de Interest creado exitosamente.',
            'url': self.success_url
        }
        if is_ajax(self.request):
            return JsonResponse(data)
        else:
            return response
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edición de un Sitio de Interest'
        context['entity'] = 'Sitio de Interest'
        context['list_url'] = reverse_lazy('dashboard:place_list')
        context['form'] = self.form_class(instance=self.object)
        return context

class PlaceDeleteView(DeleteView):
    model = PlacesOfInterest
    # template_name = 'back/delete.html'
    success_url = reverse_lazy('dashboard:place_list')
    

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.delete()
        return HttpResponseRedirect(success_url)

# Eventos
class EventoListView(ListView):
    model = Evento
    template_name = 'back/eventos/viewer.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado Eventos'
        context['create_url'] = reverse_lazy('dashboard:evento_create')
        context['delete_url'] = reverse_lazy('dashboard:evento_delete',args=[0])
        return context
    
class EventoCreateView(CreateView):
    model = Evento
    form_class = EventoForm
    template_name = 'back/components/create_update.html'
    success_url = reverse_lazy('dashboard:eventos_list')

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
        context['title'] = 'Crear Evento'
        context['entity'] = 'Evento'
        context['list_url'] = reverse_lazy('dashboard:eventos_list')
        context['action'] = 'add'
        return context

class EventoDeleteView(DeleteView):
    model = Evento
    success_url = reverse_lazy('dashboard:eventos_list')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.delete()
        return HttpResponseRedirect(success_url)


def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

class EventoUpdateView(UpdateView):
    model = Evento
    form_class = EventoForm
    template_name = 'back/components/create_update.html'
    success_url = reverse_lazy('dashboard:eventos_list')

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
        context['list_url'] = reverse_lazy('dashboard:eventos_list')
        return context


# Noticias
class NoticiaListView(ListView):
    model = Noticia
    template_name = 'back/noticias/viewer.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado Noticias'
        context['create_url'] =  reverse_lazy('dashboard:noticia_create')
        return context
    

class NoticiaCreateView(CreateView):
    model = Noticia
    form_class = NoticiaForm
    template_name = 'back/components/create_update.html'
    success_url = reverse_lazy('dashboard:noticias_list')

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
        context['title'] = 'Crear una Noticia'
        context['entity'] = 'Noticia'
        context['list_url'] = reverse_lazy('dashboard:noticias_list')
        context['action'] = 'add'
        return context
    
class NoticiaDeleteView(DeleteView):
    model = Noticia
    success_url = reverse_lazy('dashboard:noticias_list')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.delete()
        return HttpResponseRedirect(success_url)

class NoticiaUpdateView(UpdateView):
    model = Noticia
    form_class = NoticiaForm
    template_name = 'back/components/create_update.html'
    success_url = reverse_lazy('dashboard:noticias_list')

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
        context['list_url'] = reverse_lazy('dashboard:noticias_list')
        return context


        
class AlbaListView(ListView):
    model = Alba
    template_name = 'back/alba/list.html'
    
    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search':
                data = []
                for i in PlacesOfInterest.objects.all():
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Aechivos Protocolo Alba'
        context['create_url'] = reverse_lazy('dashboard:alba_create')
        context['entity'] = 'Alba'

        return context

class  AlbaCreateView(CreateView):
    model = Alba
    form_class = AlbaForm
    template_name = 'back/components/create_update.html'
    success_url = reverse_lazy('dashboard:alba_list')

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            self.object = form.save()
            data = {
                'success': True,
                'message': 'Archivo Alba creado exitosamente.',
                'url': self.success_url
            }
            return JsonResponse(data)
        else:
            data = {
                'success': False,
                'message': 'Hubo un error al crear un Archivo Alba.',
                'errors': form.errors
            }
            return JsonResponse(data)
        

    def form_invalid(self, form):
        print("form_invalid")
        response = super().form_invalid(form)
        data = {
            'success': False,
            'message': 'Hubo un error al crear un Archivo Alba.',
            'errors': form.errors
        }
        return JsonResponse(data)

    def form_valid(self, form):
        print("form_valid")
        response = super().form_valid(form)
        data = {
            'success': True,
            'message': 'Archivo Alba creado exitosamente.',
            'url': self.success_url
        }
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Subir Archivo Alba'
        context['entity'] = 'Alba'
        context['list_url'] = reverse_lazy('dashboard:alba_list')
        return context

class AlbaUpdateView( UpdateView):
    model = Alba
    form_class = AlbaForm
    template_name = 'back/components/create_update.html'
    success_url = reverse_lazy('dashboard:alba_list')

    def form_invalid(self, form):
        response = super().form_invalid(form)
        data = {
            'success': False,
            'message': 'Hubo un error al crear el Archivo Alba.',
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
            'message': 'Archivo Alba creado exitosamente.',
            'url': self.success_url
        }
        if is_ajax(self.request):
            return JsonResponse(data)
        else:
            return response
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edición de Archivo Alba'
        context['entity'] = 'Alba'
        context['list_url'] = reverse_lazy('dashboard:alba_list')
        context['form'] = self.form_class(instance=self.object)
        return context

class AlbaDeleteView(DeleteView):
    model = PlacesOfInterest
    # template_name = 'back/delete.html'
    success_url = reverse_lazy('dashboard:alba_list')
    

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.delete()
        return HttpResponseRedirect(success_url)