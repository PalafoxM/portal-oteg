from django.views.generic import TemplateView

class PreguntasfView(TemplateView):
    template_name = 'web/paginas/preguntasf/preguntasf.html' 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Preguntas Frecuentes'
        context['entity'] = 'Preguntas Frecuentes'
        context['img_url'] = 'img/Portada-1.png'
        context['nav_title'] = 'PREGUNTAS FRECUENTES'
        return context


