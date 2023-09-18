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
from web.views.sustentabilidad.views import *
from web.views.eniot.views import *
from web.views.entornonacional.views import *
from web.views.inventario.views import *
from web.views.eventos.views import *
from web.views.publicaciones_new.views import *
from web.views.buscador.views import *
from web.views.flujos_turisticos.views import *


urlpatterns = [
    # path('', HomeView.as_view(), name='home'),

    

    # path('solicitudes/',OtegView.as_view(), name='solicitudes'),
    path('', InicioView.as_view(), name='inicio'),
    path('oteg', OtegView.as_view(), name='oteg'),
    path('preguntasf/', PreguntasfView.as_view(), name='preguntasf'),
    path('sitios-interes/', SitiosView.as_view(), name='sitios_interes'),
    path('pdf-protocolo_alba/', PdfView.as_view(), name='pdf_protocolo_alba'),
    path('protocolo-alba/', ProtocoloAlbaView.as_view(), name='protocolo_alba'),
    # path('solicitudes/',solicitudes, name='solicitudes'),
    path('solicitudes/',SolicitudesView.as_view(), name='solicitudes'),
    path('segmento-turistico/cultural',CulturalView.as_view(), name='cultural'),
    path('segmento-turistico/naturaleza',NaturalezaView.as_view(), name='naturaleza'),
    path('segmento-turistico/deportivo',DeportivoView.as_view(), name='deportivo'),
    path('segmento-turistico/romance',RomanceView.as_view(), name='romance'),
    path('segmento-turistico/gastronomico',GastronomicoView.as_view(), name='gastronomico'),
    path('segmento-turistico/enologico',EnologicoView.as_view(), name='enologico'),
    path('segmento-turistico/wellness',WellnessView.as_view(), name='wellness'),
    path('segmento-turistico/mice',MiceView.as_view(), name='mice'),
    path('segmento-turistico/destilados',DestiladosView.as_view(), name='destilados'),
    path('segmento-turistico/',TuristicosView.as_view(), name='turisticos'),
    path('pueblos-magicos/',PueblosmagicosView.as_view(), name='pueblos_magicos'),
    
    #Publicaciones #
    path('publicaciones_new/',PublicacionesNewView.as_view(), name='publicaciones_new'),
    path('publicaciones/perfil_visistante_ciudad/<int:pk>/',PerfilVisitanteCiudad.as_view(), name='perfil_visistante_ciudad'),
    
    path('publicaciones/seccion/<int:pk>/',PublicacionesSecciones.as_view(), name='publicaciones_secciones'),
    
    path('publicaciones_pdf_viewer/<int:pk>/',PublicacionesPDFViewer.as_view(), name='publicaciones_pdf_viewer'),
    path('pdf/<int:pk>/', PDFDownloadView.as_view(), name='pdf_download'),
    path('pdf/back/<int:pk>/', PDFDownloadViewBack.as_view(), name='pdf_back'),
    path('audioDownload/<int:pk>/', AudioDownload.as_view(), name='audio_download'),
    path('excel_download/<int:pk>/', ExelDownload.as_view(), name='excel_download'),
    path('reporte_mensual_download/<int:pk>/', PDFReporteMensualDownloadView.as_view(), name='reporte_mensual_download'),

    path('perfil_visistante_ciudad/',PerfilVisitanteCiudad.as_view(), name='perfil_visistante_ciudad'),
    path('publicaciones/perfil-visistante-ciudad/<int:pk>/',PerfilVisitanteCiudad.as_view(), name='perfil_visistante_ciudad'),
    path('publicaciones-pdf-viewer/<int:pk>/',PublicacionesPDFViewer.as_view(), name='publicaciones_pdf_viewer'),
    path('pdf/<int:pk>/', PDFDownloadView.as_view(), name='pdf_download'),
    path('perfil-visistante-ciudad/',PerfilVisitanteCiudad.as_view(), name='perfil_visistante_ciudad'),
    path('potencias-eventos/',PotenciasEventos.as_view(), name='potencias-eventos'),
    path('otras-publicaciones/',OtasPublicaciones.as_view(), name='otras-publicaciones'),
    path('revista-oteg/',RevistaOTEG.as_view(), name='revista-oteg'),

    path('inventario-turistico/',InventarioTuristicoView.as_view(), name='inventario-turistico'),

    path('barometro-turistico/',BarometroTuristicoView.as_view(), name='barometro-turistico'),
    path('pdfDownload-Bar/<int:pk>/', PDFDownloadBarometro.as_view(), name='pdfDownload_Bar'),
    path('searchBar/', searchBar, name='search_bar'),


    # sustentabilidad
    path('sustentabilidad/',Sustentabilidad.as_view(), name='sustentabilidad'),
    # eniot
    path('eniot/',EniotView.as_view(), name='eniot'),
    path('eniot/memorias',MemoriasView.as_view(), name='eniot_memorias'),
    path('eniot/ponencia-eventos',PonenciaEventosView.as_view(), name='eniot_ponencia_eventos'),
    path('eniot/ultimos-eventos',EniotEventosFotosView.as_view(), name='eniot_ultimos_eventos'),
    path('eniot/pdf-viewer/<int:pk>/',MemoriasPDFViewer.as_view(), name='eniot_pdf_viewer'),
    path('eniot/ponencia-eventos/pdf-viewer/<int:pk>/',PonenciaEventosPDFViewer.as_view(), name='eniot_ponencia_eventos_pdf_viewer'),
    path('eniot/pdf-download/<int:pk>/', PDFDownloadEniot.as_view(), name='eniot_pdf_download'),
    # entorno-nacional
    path('entorno-nacional/',EntornoNacional.as_view(), name='entorno-nacional'),
    path('entorno-nacional/indicadores-economicos/',EntornoNacionalIndicadores.as_view(), name='entorno-nacional-indicadores'),
    # 
    path('search_noticias/', search_noticias, name='search_noticias'),
    path('noticias_turisticas/',NoticiasTuristicasView.as_view(), name='noticias_turisticas'),
    path('notica_viewer/<int:pk>/',NoticiaViewer.as_view(), name='notica_viewer'),
    path('search_words/', search_words, name='search_words'),
    path('reportes_mensuales/',ReportesMensualesView.as_view(), name='reportes_mensuales'),
    path('chart_data/', chart_data, name='chart_data'),
    path('barometro_viewer/<int:pk>/', BarometroViewer.as_view(), name='barometro_viewer'),

    # eventos
    path('eventos/',EventosView.as_view(), name='eventos'),
    path('eventos-list1/', eventos_list, name='eventos-list1'),

    #reportes mensuales search 
    path('reportes_mensuales_search/', search_reportes_m, name='reportes_mensuales_search'),
    #buscador 
    path('buscador_CEDOC/', search_view, name='search_view'),

    path ('flujos_turisticos/',FlujosTuristicosView.as_view(), name='flujos_turisticos'),  


    
]