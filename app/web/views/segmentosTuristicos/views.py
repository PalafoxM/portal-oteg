from django.views.generic import TemplateView

class CulturalView(TemplateView):
    template_name = 'web/paginas/segmento-turistico/cultural.html'

class NaturalezaView(TemplateView):
    template_name = 'web/paginas/segmento-turistico/naturaleza.html'

class DeportivoView(TemplateView):
    template_name = 'web/paginas/segmento-turistico/deportivo.html'

class RomanceView(TemplateView):
    template_name = 'web/paginas/segmento-turistico/romance.html'

class GastronomicoView(TemplateView):
    template_name = 'web/paginas/segmento-turistico/gastronomico.html'

class EnologicoView(TemplateView):
    template_name = 'web/paginas/segmento-turistico/enologico.html'

class WellnessView(TemplateView):
    template_name = 'web/paginas/segmento-turistico/wellness.html'

class MiceView(TemplateView):
    template_name = 'web/paginas/segmento-turistico/mice.html'

class DestiladosView(TemplateView):
    template_name = 'web/paginas/segmento-turistico/destilados.html'

class TuristicosView(TemplateView):
    template_name = 'web/paginas/segmento-turistico/segmentos-turisticos.html'

