from django.views.generic import TemplateView


class FlujosTuristicosView(TemplateView):
    template_name = 'web/paginas/flujos_turisticos/flujos_turisticos.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Flujos Turísticos'
        context['entity'] = 'Flujos Turísticos'
        context['img_url'] = 'img_nav/publicaciones.jpg'
        context['nav_title'] = "Flujos Turísticos"
        return context