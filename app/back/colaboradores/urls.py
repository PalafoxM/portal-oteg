from django.urls import path
from colaboradores.views import publicaciones_list

urlpatterns = [
    path('publicaciones/lista', publicaciones_list, name='publicacion_list'),
]