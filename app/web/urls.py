from django.urls import path
# import views
from web.views.oteg.views import *
from web.views.home.views import *
from web.views.solicitudes.views import *
from web.views.segmentosTuristicos.views import *


urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('oteg/', OtegView.as_view(), name='oteg'),
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
]