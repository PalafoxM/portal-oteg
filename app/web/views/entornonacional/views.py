from django.views.generic import TemplateView

class EntornoNacional(TemplateView):
    template_name = 'web/paginas/entorno-nacional/entorno-nacional.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['nav_title'] = 'Entorno Nacional'
        context['img_url'] = 'img_nav/foros.jpg'
        return context