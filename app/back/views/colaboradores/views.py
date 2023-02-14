from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.shortcuts import render
from back.models import  Publications
from back.forms import PublicationForm
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse_lazy

# Create your views here.
def publicaciones_list(request):
    data = {
        'title': 'Listado de Publicaciones',
        'publicaciones': Publications.objects.all()
    }
    print(reverse_lazy('dashboard:publicacion_create'))
    print(reverse_lazy('dashboard:publicacion_list'))
    return render(request, 'back/publicaciones/list.html', data)


class PublicationsListView(ListView):
    model = Publications
    template_name = 'back/publicaciones/list.html'

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def post(self, request,*args, **kwargs):
        data = {'name':'david'}
        return JsonResponse(data)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de publicaciones'
        return context

class  PublicationsCreateView(CreateView):
    model = Publications
    form_class = PublicationForm
    template_name = 'back/publicaciones/create.html'
    success_url = reverse_lazy('dashboard:publicacion_list')

    # def post(self, request, *args, **kwargs):
    #     data = {}
    #     try:
    #         action = request.POST['action']
    #         if action == 'add':
    #             form = self.get_form()
    #             data = form.save()
    #         else:
    #             data['error'] = 'No ha ingresado a ninguna opción'
    #     except Exception as e:
    #         data['error'] = str(e)
    #     return JsonResponse(data)




    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Crear Publicacion'
        context['entity'] = 'Publicacciones'
        context['list_url'] = reverse_lazy('dashboard:publicacion_list')
        context['action'] = 'add'
        return context

class PublicationUpdateView( UpdateView):
    model = Publications
    form_class = PublicationForm
    template_name = 'back/publicaciones/create.html'
    success_url = reverse_lazy('dashboard:publicacion_list')

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)


    # def post(self, request, *args, **kwargs):
    #     data = {}
    #     try:
    #         action = request.POST['action']
    #         if action == 'edit':
    #             form = self.get_form()
    #             data = form.save()
    #         else:
    #             data['error'] = 'No ha ingresado a ninguna opción'
    #     except Exception as e:
    #         data['error'] = str(e)
    #     return JsonResponse(data)
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edición una Pulicacion'
        context['entity'] = 'Publicacciones'
        context['list_url'] = reverse_lazy('dashboard:publicacion_list')
        context['action'] = 'edit'
        return context



class PublicationDeleteView(DeleteView):
    model = Publications
    template_name = 'back/publicaciones/delete.html'
    success_url = reverse_lazy('dashboard:publicacion_list')
    

    # def dispatch(self, request, *args, **kwargs):
    #     self.object = self.get_object()
    #     return super().dispatch(request, *args, **kwargs)

    # def post(self, request, *args, **kwargs):
    #     data = {}
    #     try:
    #         self.object.delete()
    #     except Exception as e:
    #         data['error'] = str(e)
    #     return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminación de una Publicación'
        context['entity'] = 'Publicaciones'
        context['list_url'] = self.success_url
        return context
