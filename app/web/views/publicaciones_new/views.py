from django.views.generic import TemplateView , View , ListView , DetailView
from back.models import SeccionesCentroDocumental



class PublicacionesNewView(TemplateView):
    template_name = 'web/paginas/publicaciones_new/publicaciones_new.html'

    model = SeccionesCentroDocumental

    def get_context_data(self, **kwargs):
        context = super(PublicacionesNewView, self).get_context_data(**kwargs)
        context['secciones'] = SeccionesCentroDocumental.objects.all()
        context['img_url'] = 'img_nav/publicaciones.jpg'
        context['nav_title'] = 'PUBLICACIONES'

        return context

