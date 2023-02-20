from django.shortcuts import render
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from back.models import  Banner, PlacesOfInterest,Evento , Noticia, Alba
from back.forms import BannerForm, PlacesOfInterestForm , NoticiaForm, AlbaForm

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
        return context

class  BannerCreateView(CreateView):
    model = Banner
    form_class = BannerForm
    template_name = 'back/form.html'
    success_url = reverse_lazy('dashboard:banner_list')

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'add':
                form = self.get_form()
                if form.is_valid():
                    form.save()
                else:
                    print(' cual error '+ form.errors)
                    data['error'] = form.errors
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e) + ' que fallo?'
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
    template_name = 'back/form.html'
    success_url = reverse_lazy('dashboard:banner_list')

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'edit':
                form = self.get_form()
                if form.is_valid():
                    form.save()
                else:
                    print(' cual error '+ form.errors)
                    data['error'] = form.errors
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e) + ' que fallo?'
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edición una Pulicacion'
        context['entity'] = 'Banners'
        context['list_url'] = reverse_lazy('dashboard:banner_list')
        context['action'] = 'edit'
        return context

class BanneDeleteView(DeleteView):
    model = Banner
    template_name = 'back/delete.html'
    success_url = reverse_lazy('dashboard:banner_list')
    
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            self.object.delete()
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminación de una Publicación'
        context['entity'] = 'Publicaciones'
        context['list_url'] = self.success_url
        return context

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
    template_name = 'back/form.html' 
    success_url = reverse_lazy('dashboard:place_list')

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'add':
                form = self.get_form()
                if form.is_valid():
                    form.save()
                else:
                    print(' cual error '+ form.errors)
                    data['error'] = form.errors
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Crear un Sitio de Interest'
        context['entity'] = 'Sitio de Interes'
        context['list_url'] = reverse_lazy('dashboard:place_list')
        context['action'] = 'add'
        return context

class PlaceUpdateView( UpdateView):
    model = PlacesOfInterest
    form_class = PlacesOfInterestForm
    template_name = 'back/form.html'
    success_url = reverse_lazy('dashboard:place_list')

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'edit':
                form = self.get_form()
                if form.is_valid():
                    form.save()
                else:
                    print(' cual error '+ form.errors)
                    data['error'] = form.errors
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e) + ' que fallo?'
        return JsonResponse(data)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edición de un Sitio de Interest'
        context['entity'] = 'Sitio de Interest'
        context['list_url'] = reverse_lazy('dashboard:place_list')
        context['action'] = 'edit'
        return context

class PlaceDeleteView(DeleteView):
    model = PlacesOfInterest
    template_name = 'back/delete.html'
    success_url = reverse_lazy('dashboard:place_list')
    

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            self.object.delete()
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminación de un Sitio de Interest'
        context['entity'] = 'Sitio de Interest'
        context['list_url'] = self.success_url
        return context


class EventoListView(ListView):
    model = Evento
    template_name = 'back/eventos/list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado Eventos'
        return context

class NoticiaListView(ListView):
    model = Noticia
    template_name = 'back/noticias/list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado Noticias'
        context['create_url'] =  reverse_lazy('dashboard:noticia_create')
        return context
    

class NoticiaCreateView(CreateView):
    model = Noticia
    form_class = NoticiaForm
    template_name = 'back/publicaciones/create.html'
    success_url = reverse_lazy('dashboard:noticias_list')


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Crear una Noticia'
        context['entity'] = 'Noticia'
        context['list_url'] = reverse_lazy('dashboard:noticias_list')
        context['action'] = 'add'
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
    template_name = 'back/form.html'
    success_url = reverse_lazy('dashboard:alba_list')

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'add':
                form = self.get_form()
                if form.is_valid():
                    form.save()
                else:
                    print(' cual error '+ form.errors)
                    data['error'] = form.errors
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e) + ' que fallo?'
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Subir Archivo Alba'
        context['entity'] = 'Alba'
        context['list_url'] = reverse_lazy('dashboard:alba_list')
        context['action'] = 'add'
        return context

class AlbaUpdateView( UpdateView):
    model = Alba
    form_class = AlbaForm
    template_name = 'back/form.html'
    success_url = reverse_lazy('dashboard:alba_list')

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'edit':
                form = self.get_form()
                if form.is_valid():
                    form.save()
                else:
                    print(' cual error '+ form.errors)
                    data['error'] = form.errors
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edición de Archivo Alba'
        context['entity'] = 'Alba'
        context['list_url'] = reverse_lazy('dashboard:alba_list')
        context['action'] = 'edit'
        return context

class AlbaDeleteView(DeleteView):
    model = PlacesOfInterest
    template_name = 'back/delete.html'
    success_url = reverse_lazy('dashboard:alba_list')
    

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            self.object.delete()
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminación de archivo Alba'
        context['entity'] = 'Alba'
        context['list_url'] = self.success_url
        return context