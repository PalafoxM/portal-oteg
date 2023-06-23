from django.views.generic import TemplateView , View 



class PublicacionesNewView(TemplateView):
    template_name = 'web/paginas/publicaciones_new/publicaciones_new.html'

    def get_context_data(self, **kwargs):
        context = super(PublicacionesNewView, self).get_context_data(**kwargs)
        context['publicaciones'] = ""
        return context

