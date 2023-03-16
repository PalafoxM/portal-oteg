from django.views.generic import TemplateView
from back.models import Evento
from django.http import JsonResponse
from django.views.decorators.http import require_GET


class EventosView(TemplateView):
    # model = Evento
    template_name = 'web/paginas/eventos/eventos.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eventos'
        context['entity'] = 'Eventos'
        return context

@require_GET
def eventos_list(request):

    eventos = Evento.objects.filter()
    datos = []

    for evento in eventos:
        datos.append(evento.toJSON())
    print(datos)
    return JsonResponse(datos, safe=False)