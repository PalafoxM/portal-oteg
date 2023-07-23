from django.shortcuts import render
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from back.models import *
from back.forms import *
from web.models import *
from django.contrib.auth.decorators import login_required, permission_required
from django.utils.decorators import method_decorator
from django.http import Http404
from django.core.exceptions import PermissionDenied
from back.mixins import *
from django.contrib.auth.decorators import user_passes_test

def es_admin_o_superadmin(user):
    return user.is_authenticated and (user.is_staff or user.is_superuser)


def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

# Create your views here.
class BannerListView(SuperAdminOrAdminMixin, LoginRequiredMixin, ListView):
    model = Banner
    template_name = 'back/banner/list.html'

    def dispatch(self, request, *args, **kwargs):
        try:
            return super().dispatch(request, *args, **kwargs)
        except PermissionDenied:
            raise Http404('No tiene permisos para acceder a esta página.')

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
        context['d_route'] = 'Contenido  > Banners'
        return context


class BannerCreateView(SuperAdminOrAdminMixin, LoginRequiredMixin, CreateView):
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
        context['d_route'] = 'Contenido  > Banners'
        return context


class BannerUpdateView(SuperAdminOrAdminMixin, LoginRequiredMixin, UpdateView):
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
        context['title'] = 'Edición de Banner'
        context['entity'] = 'Banners'
        context['list_url'] = reverse_lazy('dashboard:banner_list')
        context['form'] = self.form_class(instance=self.object)
        context['d_route'] = 'Contenido  > Banners'
        return context


class BanneDeleteView(SuperAdminOrAdminMixin, LoginRequiredMixin, DeleteView):
    model = Banner
    # template_name = 'back/delete.html'
    success_url = reverse_lazy('dashboard:banner_list')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.delete()
        return HttpResponseRedirect(success_url)


class PlaceListView(SuperAdminOrAdminMixin, LoginRequiredMixin, ListView):
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


class PlaceCreateView(SuperAdminOrAdminMixin, LoginRequiredMixin, CreateView):
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


class PlaceUpdateView(SuperAdminOrAdminMixin, LoginRequiredMixin, UpdateView):
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


class PlaceDeleteView(SuperAdminOrAdminMixin, LoginRequiredMixin, DeleteView):
    model = PlacesOfInterest
    # template_name = 'back/delete.html'
    success_url = reverse_lazy('dashboard:place_list')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.delete()
        return HttpResponseRedirect(success_url)

# Eventos


class EventoListView(SuperAdminOrAdminMixin, LoginRequiredMixin, ListView):
    model = Evento
    template_name = 'back/eventos/viewer.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado Eventos'
        context['create_url'] = reverse_lazy('dashboard:evento_create')
        context['delete_url'] = reverse_lazy(
            'dashboard:evento_delete', args=[0])
        context['d_route'] = 'Contenido > Eventos'
        return context


class EventoCreateView(SuperAdminOrAdminMixin, LoginRequiredMixin, CreateView):
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
        context['d_route'] = 'Contenido > Eventos'
        return context


class EventoDeleteView(SuperAdminOrAdminMixin, LoginRequiredMixin, DeleteView):
    model = Evento
    success_url = reverse_lazy('dashboard:eventos_list')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.delete()
        return HttpResponseRedirect(success_url)


def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'


class EventoUpdateView(SuperAdminOrAdminMixin, LoginRequiredMixin, UpdateView):
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
        context['d_route'] = 'Contenido > Eventos'
        return context


# Noticias

class NoticiaListView(SuperAdminOrAdminMixin, LoginRequiredMixin, ListView):
    model = Noticia
    template_name = 'back/noticias/viewer.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado Noticias'
        context['create_url'] = reverse_lazy('dashboard:noticia_create')
        context['d_route'] = 'Contenido > Noticias'
        return context


class NoticiaCreateView(SuperAdminOrAdminMixin, LoginRequiredMixin, CreateView):
    model = Noticia
    form_class = NoticiaForm
    template_name = 'back/components/create_update_CKE.html'
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
        context['d_route'] = 'Contenido > Noticias'
        return context


class NoticiaDeleteView(SuperAdminOrAdminMixin, LoginRequiredMixin, DeleteView):
    model = Noticia
    success_url = reverse_lazy('dashboard:noticias_list')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.delete()
        return HttpResponseRedirect(success_url)


class NoticiaUpdateView(SuperAdminOrAdminMixin, LoginRequiredMixin, UpdateView):
    model = Noticia
    form_class = NoticiaForm
    template_name = 'back/components/create_update_CKE.html'
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
        context['d_route'] = 'Contenido > Noticias'
        return context

# Glosario


class GlosarioListView(SuperAdminOrAdminMixin, LoginRequiredMixin, ListView):
    model = Glosario
    template_name = 'back/glosario/viewer.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado Glosario'
        context['create_url'] = reverse_lazy('dashboard:glosario_create')
        context['d_route'] = 'Otros > Glosario'
        return context


class GlosarioCreateView(SuperAdminOrAdminMixin, LoginRequiredMixin, CreateView):
    model = Glosario
    form_class = GlosarioForm
    template_name = 'back/components/create_update.html'
    success_url = reverse_lazy('dashboard:glosario_list')

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            self.object = form.save()
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
        context['title'] = 'Crear una Palabra'
        context['entity'] = 'Glosario'
        context['list_url'] = reverse_lazy('dashboard:glosario_list')
        context['action'] = 'add'
        context['d_route'] = 'Otros > Glosario'
        return context


class GlosarioDeleteView(SuperAdminOrAdminMixin, LoginRequiredMixin, DeleteView):
    model = Glosario
    success_url = reverse_lazy('dashboard:glosario_list')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.delete()
        return HttpResponseRedirect(success_url)


class GlosarioUpdateView(SuperAdminOrAdminMixin, LoginRequiredMixin, UpdateView):
    model = Glosario
    form_class = GlosarioForm
    template_name = 'back/components/create_update.html'
    success_url = reverse_lazy('dashboard:glosario_list')

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
        context['list_url'] = reverse_lazy('dashboard:glosario_list')
        context['d_route'] = 'Otros > Glosario'
        return context


class BarometroListView(SuperAdminOrAdminMixin, LoginRequiredMixin, ListView):
    model = BarometroTuristico
    template_name = 'back/barometro/viewer.html'

    try:
        encuesta = Encuesta.objects.filter(seccion=1, activo=True).latest('fecha_registro')
        print(encuesta.seccion)
    except Encuesta.DoesNotExist:
        encuesta = None
        print("No matching Encuesta found.")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado Barometro'
        context['create_url'] = reverse_lazy('dashboard:barometro_create')
        context['encuesta'] = self.encuesta
        context['d_route'] = 'CEDOC > Barometro'
    

        return context


class BarometroCreateView(SuperAdminOrAdminMixin, LoginRequiredMixin, CreateView):
    model = BarometroTuristico
    form_class = BarometroForm
    template_name = 'back/components/create_update.html'
    success_url = reverse_lazy('dashboard:barometro_list')

    def post(self, request, *args, **kwargs):
        # Incluir request.FILES para manejar los archivos subidos
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            self.object = form.save()
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
        context['title'] = 'Crear una Documento'
        context['entity'] = 'Barometro'
        context['list_url'] = reverse_lazy('dashboard:barometro_list')
        context['action'] = 'add'
        context['d_route'] = 'CEDOC > Barometro'
        return context


class BarometroDeleteView(SuperAdminOrAdminMixin, LoginRequiredMixin, DeleteView):
    model = BarometroTuristico
    success_url = reverse_lazy('dashboard:barometro_list')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.delete()
        return HttpResponseRedirect(success_url)


class BarometroUpdateView(SuperAdminOrAdminMixin, LoginRequiredMixin, UpdateView):
    model = BarometroTuristico
    form_class = BarometroForm
    template_name = 'back/components/create_update.html'
    success_url = reverse_lazy('dashboard:barometro_list')

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
        context['list_url'] = reverse_lazy('dashboard:barometro_list')
        context['d_route'] = 'CEDOC > Barometro'
        context['title'] = 'Editar un Documento'
        return context

