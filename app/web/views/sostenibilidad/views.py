from django.views.generic import TemplateView

class Sostenibilidad(TemplateView):
    template_name = 'web/paginas/sostenibilidad/sostenibilidad.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['nav_title'] = 'SOSTENIBILIDAD'
        context['img_url'] = 'img_nav/Artesanias_Guanajuato_19.JPG'
        return context