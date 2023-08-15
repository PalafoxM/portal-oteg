from django.views.generic import TemplateView

class Sustentabilidad(TemplateView):
    template_name = 'web/paginas/sustentabilidad/sustentabilidad.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['nav_title'] = 'SUSTENTABILIDAD'
        context['img_url'] = 'img_nav/11Torito_Sustentabilidad.jpg'
        return context