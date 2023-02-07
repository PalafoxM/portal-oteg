from django.urls import path
from colaboradores.views import *

app_name = 'colaboradores'

urlpatterns = [
    path('publicaciones/lista', publicaciones_list, name='publicacion_list'),
    path('publicaciones/add', PublicationsCreateView.as_view(), name='publicacion_create'),
    path('publicaciones/edit/<int:pk>/', PublicationUpdateView.as_view(), name='publicacion_update'),
    path('publicaciones/delete/<int:pk>/', PublicationDeleteView.as_view(), name='publicacion_delete'),
]