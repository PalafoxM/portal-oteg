from django.urls import path
# import views
from web.views.oteg.views import *
from web.views.home.views import *
from web.views.inicio.views import *
from web.views.preguntas_f.views import *
from web.views.sitios_interes.views import *
from web.views.protocoloalba.views import *

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('oteg/', OtegView.as_view(), name='oteg'),
    path('solicitudes/',OtegView.as_view(), name='solicitudes'),
    path('inicio/', InicioView.as_view(), name='inicio'),
    path('preguntasf/', PreguntasfView.as_view(), name='preguntasf'),
    path('sitios_interes/', SitiosView.as_view(), name='sitios_interes'),
    path('pdf_protocolo_alba/', PdfView.as_view(), name='pdf_protocolo_alba'),
    path('protocolo_alba/', ProtocoloAlbaView.as_view(), name='protocolo_alba'),
]