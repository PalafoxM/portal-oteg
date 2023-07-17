from django.views.generic import TemplateView

class OtegView(TemplateView):
    template_name = 'web/paginas/oteg/oteg.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'OTEG'
        context['entity'] = 'OTEG'
        context['img_url'] = 'img_nav/publicaciones.jpg'
        context['nav_title'] = 'OTEG'
        return context

