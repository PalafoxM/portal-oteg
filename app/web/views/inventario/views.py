from django.views.generic import TemplateView

class InventarioTuristico(TemplateView):
    template_name = 'web/paginas/inventario/inventario.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['nav_title'] = 'INVENTARIO TURÍSTICO'
        context['img_url'] = 'img/Portada-3.png'
        return context
