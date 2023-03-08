from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.shortcuts import render
from back.models import  Publications
from back.forms import PublicationForm
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse_lazy

# Create your views here.
class PublicationsListView(ListView):
    model = Publications
    template_name = 'back/publicaciones/list.html' 

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search':
                data = []
                for i in Publications.objects.all():
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de publicaciones'
        context['create_url'] = reverse_lazy('dashboard:publicacion_create')
        context['entity'] = 'Publicaciones'
        return context

class  PublicationsCreateView(CreateView):
    model = Publications
    form_class = PublicationForm
    template_name = 'back/components/create_update.html'
    success_url = reverse_lazy('dashboard:publicacion_list')

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            self.object = form.save()
            data = {
                'success': True,
                'message': 'Publicacion creada exitosamente.',
                'url': self.success_url
            }
            return JsonResponse(data)
        else:
            data = {
                'success': False,
                'message': 'Hubo un error al crear una Publicacion.',
                'errors': form.errors
            }
            return JsonResponse(data)
        

    def form_invalid(self, form):
        print("form_invalid")
        response = super().form_invalid(form)
        data = {
            'success': False,
            'message': 'Hubo un error al crear una Publicacion.',
            'errors': form.errors
        }
        return JsonResponse(data)

    def form_valid(self, form):
        print("form_valid")
        response = super().form_valid(form)
        data = {
            'success': True,
            'message': 'Publicacion creada exitosamente.',
            'url': self.success_url
        }
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Crear Publicacion'
        context['entity'] = 'Publicacciones'
        context['list_url'] = reverse_lazy('dashboard:publicacion_list')
        context['action'] = 'add'
        return context


def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

class PublicationUpdateView( UpdateView):
    model = Publications
    form_class = PublicationForm
    template_name = 'back/components/create_update.html'
    success_url = reverse_lazy('dashboard:publicacion_list')

    def form_invalid(self, form):
        response = super().form_invalid(form)
        data = {
            'success': False,
            'message': 'Hubo un error al crear la Publicación.',
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
            'message': 'Publicación creada exitosamente.',
            'url': self.success_url
        }
        if is_ajax(self.request):
            return JsonResponse(data)
        else:
            return response
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edición una Pulicacion'
        context['entity'] = 'Publicacciones'
        context['list_url'] = reverse_lazy('dashboard:publicacion_list')
        context['form'] = self.form_class(instance=self.object)
        return context



class PublicationDeleteView(DeleteView):
    model = Publications
    # template_name = 'back/delete.html'
    success_url = reverse_lazy('dashboard:publicacion_list')
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.delete()
        return HttpResponseRedirect(success_url)
