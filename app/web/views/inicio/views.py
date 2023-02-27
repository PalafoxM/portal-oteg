from django.views.generic import TemplateView
from django.urls import reverse_lazy
from django.db.models import F
from back.models import Banner ,Noticia

class InicioView(TemplateView):
    model = Banner
    model2 = Noticia
    template_name = 'web/paginas/inicio/inicio.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Inicio'
        context['banners'] = Banner.objects.filter(publication=True) #order By date
        context['noticias'] = Noticia.objects.order_by(F('fecha_recuperacion').desc(nulls_last=True))[:5] # order by date
        context['data'] = int(85)
        context['data2'] = int(18.66)
        return context
