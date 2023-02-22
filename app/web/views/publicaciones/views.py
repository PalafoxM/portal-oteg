from django.views.generic import TemplateView


class PerfilVisitanteCiudad (TemplateView):
    template_name = 'web/paginas/publicaciones/perfil_visitante_ciudad.html'

class PotenciasEventos (TemplateView):
    template_name = 'web/paginas/publicaciones/ponencias_eventos.html'

class RevistaOTEG (TemplateView):
    template_name = 'web/paginas/publicaciones/revista_oteg.html'

class OtasPublicaciones (TemplateView):
    template_name = 'web/paginas/publicaciones/otras_publicaciones.html'

class InventarioTuristico (TemplateView):
    template_name = 'web/paginas/publicaciones/inventario_turistico.html'