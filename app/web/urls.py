from django.urls import path
# import views
from web.views.oteg.views import *
from web.views.home.views import *
from web.views.inicio.views import *
from web.views.preguntas_f.views import *
from web.views.sitios_interes.views import *
from web.views.protocoloalba.views import *
from web.views.solicitudes.views import *
from web.views.segmentosTuristicos.views import *
from web.views.pueblos_magicos.views import *
from web.views.publicaciones.views import *


urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('oteg/', OtegView.as_view(), name='oteg'),
    path('solicitudes/',OtegView.as_view(), name='solicitudes'),
    path('inicio/', InicioView.as_view(), name='inicio'),
    path('preguntasf/', PreguntasfView.as_view(), name='preguntasf'),
    path('sitios_interes/', SitiosView.as_view(), name='sitios_interes'),
    path('pdf_protocolo_alba/', PdfView.as_view(), name='pdf_protocolo_alba'),
    path('protocolo_alba/', ProtocoloAlbaView.as_view(), name='protocolo_alba'),
    path('solicitudes/',solicitudes, name='solicitudes'),
    path('segmento-turistico/cultural',CulturalView.as_view(), name='cultural'),
    path('segmento-turistico/naturaleza',NaturalezaView.as_view(), name='naturaleza'),
    path('segmento-turistico/deportivo',DeportivoView.as_view(), name='deportivo'),
    path('segmento-turistico/romance',RomanceView.as_view(), name='romance'),
    path('segmento-turistico/gastronomico',GastronomicoView.as_view(), name='gastronomico'),
    path('segmento-turistico/enologico',EnologicoView.as_view(), name='enologico'),
    path('segmento-turistico/wellness',WellnessView.as_view(), name='wellness'),
    path('segmento-turistico/mice',MiceView.as_view(), name='mice'),
    path('segmento-turistico/destilados',DestiladosView.as_view(), name='destilados'),
    path('segmento-turistico/segmentos-turisticos',TuristicosView.as_view(), name='turisticos'),
    path('pueblos-magicos/',PueblosmagicosView.as_view(), name='pueblos_magicos'),
    #Publicaciones
    path('publicaciones/perfil_visistante_ciudad/<int:pk>/',PerfilVisitanteCiudad.as_view(), name='perfil_visistante_ciudad'),
    path('publicaciones_pdf_viewer/<int:pk>/',PublicacionesPDFViewer.as_view(), name='publicaciones_pdf_viewer'),
    path('pdf/<int:pk>/', PDFDownloadView.as_view(), name='pdf_download'),
    path('perfil_visistante_ciudad/',PerfilVisitanteCiudad.as_view(), name='perfil_visistante_ciudad'),
    path('potencias-eventos/',PotenciasEventos.as_view(), name='potencias-eventos'),
    path('otras-publicaciones/',OtasPublicaciones.as_view(), name='otras-publicaciones'),
    path('revista-oteg/',RevistaOTEG.as_view(), name='revista-oteg'),
    path('inventario-turistico/',InventarioTuristico.as_view(), name='inventario-turistico'),
    path('barometro-turistico/',BarometroTuristicoView.as_view(), name='barometro-turistico'),
    path('pdfDownload_Bar/<int:pk>/', PDFDownloadBarometro.as_view(), name='pdfDownload_Bar'),
    path('search/', search, name='search'),
    path('search_noticias/', search_noticias, name='search_noticias'),
    path('noticias_turisticas/',NoticiasTuristicasView.as_view(), name='noticias_turisticas'),
    path('search_words/', search_words, name='search_words'),
    path('reportes_mensuales/',ReportesMensualesView.as_view(), name='reportes_mensuales'),
    path('chart_data/', chart_data, name='chart_data'),


]