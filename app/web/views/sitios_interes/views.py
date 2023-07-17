from django.views.generic import TemplateView

class SitiosView(TemplateView):
    template_name = 'web/paginas/sitios_interes/sitios_interes.html'

    def get_context_data(self, **kwargs):
        context = super(SitiosView, self).get_context_data(**kwargs)
        context['nav_title'] = 'SITIOS DE INTERÉS'
        context['img_url'] = 'img_nav/preguntas.png'
        return context