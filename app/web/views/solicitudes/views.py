from django.shortcuts import render, redirect
from web.forms  import SenEmail

from django.core.mail import BadHeaderError, send_mail, EmailMultiAlternatives
from django.http import JsonResponse, HttpResponse
from django.template.loader import get_template
from django.conf import  settings
from django.contrib import messages
from django.views import View

# Create your views here.
def solicitudes(request):
    if request.method == "POST":
        # 
        form = SenEmail(request.POST)
        if form.is_valid():
            try:
                # creamos un modelo para el template de correo
                context = {
                    'Email': request.POST.get('email'),
                    'name': request.POST.get('subject'),
                    'contry': request.POST.get('contry'),
                    'message': request.POST.get('message'),
                }
                print(request.POST.get('message'))
                # agregamos los parametros
                subject, from_email, to = 'Solicitud de Informacion', settings.EMAIL_HOST_USER, settings.CORREO_DESTINO
                # contenuido del mensaje
                text_content = request.POST.get('message')
                # plantilla del mensaje
                html_content = get_template('web/correo.html')
                # mandamos la informacion a la plantillas
                content = html_content.render(context)
                # creamos la instancia del mensaje
                msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
                # indicamos que va usar html
                msg.attach_alternative(content, "text/html")
                # mandamos el mensaje
                msg.send()
                messages.success(request, 'Solicitud enviada exitosamente.')
                return redirect('solicitudes')
            except BadHeaderError:
                print("trono?")
                return HttpResponse('Invalid header found.')
            print("si pasaron")
    else:
        form = SenEmail()
    
    context = {
        'form': form,
        'nav_title': 'SOLICITUDES DE INFORMACIÓN',
        'img_url': 'img_nav/arana.jpg',
        'subtitulo': True
    }

    return render(request, 'web/paginas/solicitudes.html', context)

class SolicitudesView(View):
    template_name = 'web/paginas/solicitudes.html'

    def post(self, request, *args, **kwargs):
        form = SenEmail(request.POST)
        if form.is_valid():
            try:
                # Creamos un modelo para el template de correo
                context = {
                    'Email': request.POST.get('email'),
                    'name': request.POST.get('subject'),
                    'contry': request.POST.get('contry'),
                    'message': request.POST.get('message'),
                }

                # Contenido del mensaje
                text_content = request.POST.get('message')

                # Plantilla del mensaje
                html_content = get_template('web/correo.html')

                # Mandamos la información a la plantilla
                content = html_content.render(context)

                # Creamos la instancia del mensaje
                subject, from_email, to = 'Solicitud de Informacion', settings.EMAIL_HOST_USER, settings.CORREO_DESTINO
                msg = EmailMultiAlternatives(subject, text_content, from_email, [to])

                # Indicamos que va a usar HTML
                msg.attach_alternative(content, "text/html")

                # Mandamos el mensaje
                msg.send()

                # Enviamos una respuesta JSON en caso de éxito
                response_data = {
                    'success': True,
                    'message': 'Solicitud enviada exitosamente.',
                }
                return JsonResponse(response_data)

            except BadHeaderError:
                return JsonResponse({'success': False, 'message': 'Invalid header found.'})

        # Enviamos una respuesta JSON en caso de error en el formulario
        response_data = {
            'success': False,
            'message': 'Error en el formulario.',
            'errors': form.errors,
        }
        return JsonResponse(response_data)

    def get(self, request, *args, **kwargs):
        form = SenEmail()
        context = {
            'form': form,
            'nav_title': 'SOLICITUDES DE INFORMACIÓN',
            'img_url': 'img_nav/arana.jpg',
            'subtitulo': True,
        }
        return render(request, self.template_name, context)