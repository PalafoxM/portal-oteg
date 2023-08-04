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
        context['img_url'] = 'img_nav/festival-globos.jpg'
        return context

@require_GET
def eventos_list(request):
    eventos = Evento.objects.all()
    datos = []

    for evento in eventos:
        evento_data = evento.toJSON()
        
        # Si el campo 'imagen' es un campo de imagen proporcionado por Django (por ejemplo, models.ImageField)
        # Puedes acceder a la URL de la imagen almacenada en S3 utilizando 'evento.imagen.url'
        if evento.imagen:
            imagen_s3_url = evento.imagen.url
            evento_data['imagen'] = imagen_s3_url
        
        datos.append(evento_data)
    
    return JsonResponse(datos, safe=False)