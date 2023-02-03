from django.urls import path
from colaboradores.views import publicaciones_list
from contenido.views import homeAdmin

urlpatterns = [
    path('', homeAdmin, name='homeAdmin'),
    path('publicaciones/lista', publicaciones_list, name='publicacion_list'),
]