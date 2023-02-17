from django.views.generic import TemplateView
from django.urls import reverse_lazy
from back.models import Banner

class InicioView(TemplateView):
    model = Banner
    template_name = 'web/paginas/inicio/inicio.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Inicio'
        context['banners'] = Banner.objects.filter(publication=True)
        context['data'] = 85
        context['data2'] = 18.665

        return context
