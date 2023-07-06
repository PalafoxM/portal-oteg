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

from django.contrib.auth.decorators import user_passes_test

def es_admin_o_superadmin(user):
    return user.is_authenticated and (user.is_staff or user.is_superuser)

def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

# Create your views here.
@method_decorator(login_required(login_url='/auth/login_user'), name='dispatch')
@method_decorator(permission_required('auth.view_banner', raise_exception=True), name='dispatch')
@method_decorator(user_passes_test(es_admin_o_superadmin, login_url='404'), name='dispatch')
class BannerListView(ListView):
    model = Banner
    template_name = 'back/banner/list.html'
    
    def dispatch(self, request, *args, **kwargs):
        try:
            return super().dispatch(request, *args, **kwargs)
        except PermissionDenied:
            raise Http404

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


@method_decorator(login_required(login_url='/auth/login_user'), name='dispatch')
@method_decorator(permission_required('auth.view_banner', raise_exception=True), name='dispatch')
@method_decorator(user_passes_test(es_admin_o_superadmin, login_url='404'), name='dispatch')
class BannerCreateView(CreateView):
    model = Banner
    form_class = BannerForm
    template_name = 'back/banner/create_update.html'
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

@method_decorator(login_required(login_url='/auth/login_user'), name='dispatch')
@method_decorator(permission_required('auth.view_banner', raise_exception=True), name='dispatch')
@method_decorator(user_passes_test(es_admin_o_superadmin, login_url='404'), name='dispatch')
class BannerUpdateView(UpdateView):
    model = Banner
    form_class = BannerForm
    template_name = 'back/banner/create_update.html'
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

@method_decorator(login_required(login_url='/auth/login_user'), name='dispatch')
@method_decorator(permission_required('auth.view_banner', raise_exception=True), name='dispatch')
@method_decorator(user_passes_test(es_admin_o_superadmin, login_url='404'), name='dispatch')
class BanneDeleteView(DeleteView):
    model = Banner
    # template_name = 'back/delete.html'
    success_url = reverse_lazy('dashboard:banner_list')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.delete()
        return HttpResponseRedirect(success_url)

@method_decorator(login_required(login_url='/auth/login_user'), name='dispatch')
@method_decorator(permission_required('auth.view_banner', raise_exception=True), name='dispatch')
@method_decorator(user_passes_test(es_admin_o_superadmin, login_url='404'), name='dispatch')
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

@method_decorator(login_required(login_url='/auth/login_user'), name='dispatch')
@method_decorator(permission_required('auth.view_banner', raise_exception=True), name='dispatch')
@method_decorator(user_passes_test(es_admin_o_superadmin, login_url='404'), name='dispatch')
class PlaceCreateView(CreateView):
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

@method_decorator(login_required(login_url='/auth/login_user'), name='dispatch')
@method_decorator(permission_required('auth.view_banner', raise_exception=True), name='dispatch')
@method_decorator(user_passes_test(es_admin_o_superadmin, login_url='404'), name='dispatch')
class PlaceUpdateView(UpdateView):
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

@method_decorator(login_required(login_url='/auth/login_user'), name='dispatch')
@method_decorator(permission_required('auth.view_banner', raise_exception=True), name='dispatch')
@method_decorator(user_passes_test(es_admin_o_superadmin, login_url='404'), name='dispatch')
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

@method_decorator(login_required(login_url='/auth/login_user'), name='dispatch')
@method_decorator(permission_required('auth.view_banner', raise_exception=True), name='dispatch')
@method_decorator(user_passes_test(es_admin_o_superadmin, login_url='404'), name='dispatch')
class EventoListView(ListView):
    model = Evento
    template_name = 'back/eventos/viewer.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado Eventos'
        context['create_url'] = reverse_lazy('dashboard:evento_create')
        context['delete_url'] = reverse_lazy(
            'dashboard:evento_delete', args=[0])
        return context

@method_decorator(login_required(login_url='/auth/login_user'), name='dispatch')
@method_decorator(permission_required('auth.view_banner', raise_exception=True), name='dispatch')
@method_decorator(user_passes_test(es_admin_o_superadmin, login_url='404'), name='dispatch')
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

@method_decorator(login_required(login_url='/auth/login_user'), name='dispatch')
@method_decorator(permission_required('auth.view_banner', raise_exception=True), name='dispatch')
@method_decorator(user_passes_test(es_admin_o_superadmin, login_url='404'), name='dispatch')
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

@method_decorator(login_required(login_url='/auth/login_user'), name='dispatch')
@method_decorator(permission_required('auth.view_banner', raise_exception=True), name='dispatch')
@method_decorator(user_passes_test(es_admin_o_superadmin, login_url='404'), name='dispatch')
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
@method_decorator(login_required(login_url='/auth/login_user'), name='dispatch')
@method_decorator(permission_required('auth.view_banner', raise_exception=True), name='dispatch')
@method_decorator(user_passes_test(es_admin_o_superadmin, login_url='404'), name='dispatch')
class NoticiaListView(ListView):
    model = Noticia
    template_name = 'back/noticias/viewer.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado Noticias'
        context['create_url'] = reverse_lazy('dashboard:noticia_create')
        return context

@method_decorator(login_required(login_url='/auth/login_user'), name='dispatch')
@method_decorator(permission_required('auth.view_banner', raise_exception=True), name='dispatch')
@method_decorator(user_passes_test(es_admin_o_superadmin, login_url='404'), name='dispatch')
class NoticiaCreateView(CreateView):
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
        return context

@method_decorator(login_required(login_url='/auth/login_user'), name='dispatch')
@method_decorator(permission_required('auth.view_banner', raise_exception=True), name='dispatch')
@method_decorator(user_passes_test(es_admin_o_superadmin, login_url='404'), name='dispatch')
class NoticiaDeleteView(DeleteView):
    model = Noticia
    success_url = reverse_lazy('dashboard:noticias_list')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.delete()
        return HttpResponseRedirect(success_url)

@method_decorator(login_required(login_url='/auth/login_user'), name='dispatch')
@method_decorator(permission_required('auth.view_banner', raise_exception=True), name='dispatch')
@method_decorator(user_passes_test(es_admin_o_superadmin, login_url='404'), name='dispatch')
class NoticiaUpdateView(UpdateView):
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
        return context

# Glosario

@method_decorator(login_required(login_url='/auth/login_user'), name='dispatch')
@method_decorator(permission_required('auth.view_banner', raise_exception=True), name='dispatch')
@method_decorator(user_passes_test(es_admin_o_superadmin, login_url='404'), name='dispatch')
class GlosarioListView(ListView):
    model = Glosario
    template_name = 'back/glosario/viewer.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado Glosario'
        context['create_url'] = reverse_lazy('dashboard:glosario_create')
        return context

@method_decorator(login_required(login_url='/auth/login_user'), name='dispatch')
@method_decorator(permission_required('auth.view_banner', raise_exception=True), name='dispatch')
@method_decorator(user_passes_test(es_admin_o_superadmin, login_url='404'), name='dispatch')
class GlosarioCreateView(CreateView):
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
        return context

@method_decorator(login_required(login_url='/auth/login_user'), name='dispatch')
@method_decorator(permission_required('auth.view_banner', raise_exception=True), name='dispatch')
@method_decorator(user_passes_test(es_admin_o_superadmin, login_url='404'), name='dispatch')
class GlosarioDeleteView(DeleteView):
    model = Glosario
    success_url = reverse_lazy('dashboard:glosario_list')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.delete()
        return HttpResponseRedirect(success_url)

@method_decorator(login_required(login_url='/auth/login_user'), name='dispatch')
@method_decorator(permission_required('auth.view_banner', raise_exception=True), name='dispatch')
@method_decorator(user_passes_test(es_admin_o_superadmin, login_url='404'), name='dispatch')
class GlosarioUpdateView(UpdateView):
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
        return context

@method_decorator(login_required(login_url='/auth/login_user'), name='dispatch')
@method_decorator(permission_required('auth.view_banner', raise_exception=True), name='dispatch')
@method_decorator(user_passes_test(es_admin_o_superadmin, login_url='404'), name='dispatch')
class BarometroListView(ListView):
    model = BarometroTuristico
    template_name = 'back/barometro/viewer.html'

    try:
        encuesta = Encuesta.objects.filter(seccion=1, activo=True).latest('fecha_registro')
        print(encuesta.seccion)
    except Encuesta.DoesNotExist:
        print("No matching Encuesta found.")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado Barometro'
        context['create_url'] = reverse_lazy('dashboard:barometro_create')
        context['encuesta'] = self.encuesta
    

        return context

@method_decorator(login_required(login_url='/auth/login_user'), name='dispatch')
@method_decorator(permission_required('auth.view_banner', raise_exception=True), name='dispatch')
@method_decorator(user_passes_test(es_admin_o_superadmin, login_url='404'), name='dispatch')
class BarometroCreateView(CreateView):
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
        return context

@method_decorator(login_required(login_url='/auth/login_user'), name='dispatch')
@method_decorator(permission_required('auth.view_banner', raise_exception=True), name='dispatch')
@method_decorator(user_passes_test(es_admin_o_superadmin, login_url='404'), name='dispatch')
class BarometroDeleteView(DeleteView):
    model = BarometroTuristico
    success_url = reverse_lazy('dashboard:barometro_list')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.delete()
        return HttpResponseRedirect(success_url)

@method_decorator(login_required(login_url='/auth/login_user'), name='dispatch')
@method_decorator(permission_required('auth.view_banner', raise_exception=True), name='dispatch')
@method_decorator(user_passes_test(es_admin_o_superadmin, login_url='404'), name='dispatch')
class BarometroUpdateView(UpdateView):
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
        return context

