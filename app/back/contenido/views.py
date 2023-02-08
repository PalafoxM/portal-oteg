from django.shortcuts import render
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from contenido.models import  Banner
from contenido.forms import BannerForm

# Create your views here.
def baners_list(request):
    data = {
        'title': 'Listado de Banners',
        'banners': Banner.objects.all(),
        'create_url': reverse_lazy('colaboradores:banner_create')
    }
    # print(Banner.objects.all() )
    return render(request, 'back/banner/list.html', data)


class BannerListView(ListView):
    model = Banner
    template_name = 'back/banner/list.html'

    # def dispatch(self, request, *args, **kwargs):
    #     return super().dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search':
                data = []
                for i in Banner.objects.all():
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)



    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de banners'
        return context

class  BannerCreateView(CreateView):
    model = Banner
    form_class = BannerForm
    template_name = 'back/publicaciones/create.html'
    success_url = reverse_lazy('colaboradores:banner_list')

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
        context['entity'] = 'Banners'
        context['list_url'] = reverse_lazy('colaboradores:banner_list')
        context['action'] = 'add'
        return context

class BannerUpdateView( UpdateView):
    model = Banner
    form_class = BannerForm
    template_name = 'back/publicaciones/create.html'
    success_url = reverse_lazy('colaboradores:banner_list')

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)


    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'edit':
                form = self.get_form()
                data = form.save()
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edición una Pulicacion'
        context['entity'] = 'Banners'
        context['list_url'] = reverse_lazy('colaboradores:banner_list')
        context['action'] = 'edit'
        return context



class BanneDeleteView(DeleteView):
    model = Banner
    template_name = 'back/publicaciones/delete.html'
    success_url = reverse_lazy('colaboradores:banner_list')
    

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
