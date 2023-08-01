from django.views.generic import TemplateView
from django.urls import reverse_lazy
from django.db.models import F
from back.models import Banner ,Noticia

class InicioView(TemplateView):
    model = Banner
    model2 = Noticia
    template_name = 'web/paginas/inicio/inicio_new.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Inicio'
        context['banners'] = Banner.objects.filter(activo=True).order_by('-date_created')
        context['noticias'] = Noticia.objects.order_by(F('fecha_nota').desc(nulls_last=True))[:3] # order by date
        context['is_one_new'] = True if len(context['noticias']) == 1 else False    
        context['data'] = int(85)
        context['data2'] = int(18.66)
        return context
