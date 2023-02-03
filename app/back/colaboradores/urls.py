from django.urls import path
from colaboradores.views import *

urlpatterns = [
    path('publicaciones/lista', PublicationsListView.as_view(), name='publicacion_list'),
]