from django.urls import path
# import views
from web.views.oteg.views import *
from web.views.home.views import *
from web.views.inicio.views import *

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('oteg/', OtegView.as_view(), name='oteg'),
    path('solicitudes/',OtegView.as_view(), name='solicitudes'),

    path('inicio/', InicioView.as_view(), name='inicio'),
]