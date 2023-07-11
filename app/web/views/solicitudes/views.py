from django.shortcuts import render, redirect
from web.forms  import SenEmail

from django.core.mail import BadHeaderError, send_mail, EmailMultiAlternatives
from django.http import HttpResponse
from django.template.loader import get_template
from django.conf import  settings
from django.contrib import messages

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
                return HttpResponse('Invalid header found.')
            print("si pasaron")
    else:
        form = SenEmail()
    
    context = {
        'form': form,
        'nav_title': 'SOLICITUDES DE INFROMACIÓN',
        'img_url': 'img_nav/pdf.png',
    }

    return render(request, 'web/paginas/solicitudes.html', context)