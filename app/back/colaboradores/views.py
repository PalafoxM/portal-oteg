from django.views.generic import ListView
from django.shortcuts import render
from colaboradores.models import  Publications

# Create your views here.
def publicaciones_list(request):
    data = {
        'title': 'Listado de Publicaciones',
        'publicaciones': Publications.objects.all()
    }
    return render(request, 'publicaciones/list.html', data)


class PublicationsListView(ListView):
    model = Publications
    template_name = 'publicaciones/list.html'

    def get_queryset(self):
        return Publications.objects.filter(name="1")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de publicaciones'

        return context