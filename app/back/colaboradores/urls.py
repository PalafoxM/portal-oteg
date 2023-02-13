from django.urls import path
from colaboradores.views import *
from contenido.views import *
from otros.views import *

app_name = 'colaboradores'

urlpatterns = [
    path('publicaciones/list', publicaciones_list, name='publicacion_list'),
    path('publicaciones/add', PublicationsCreateView.as_view(), name='publicacion_create'),
    path('publicaciones/edit/<int:pk>/', PublicationUpdateView.as_view(), name='publicacion_update'),
    path('publicaciones/delete/<int:pk>/', PublicationDeleteView.as_view(), name='publicacion_delete'),
    # contenido -> banner
    path('banner/list', baners_list, name='banner_list'),
    path('banner/add', BannerCreateView.as_view(), name='banner_create'),
    path('banner/edit/<int:pk>/', BannerUpdateView.as_view(), name='banner_update'),
    path('banner/delete/<int:pk>/', BanneDeleteView.as_view(), name='banner_delete'),
    # contenido -> places of interest
    path('place-of-interest/list', places_list, name='place_list'),
    path('place-of-interest/add', PlaceCreateView.as_view(), name='place_create'),
    path('place-of-interest/edit/<int:pk>/', PlaceUpdateView.as_view(), name='place_update'),
    path('place-of-interest/delete/<int:pk>/', PlaceDeleteView.as_view(), name='place_delete'),
    # otros
    path('descargas/list', descargas_list, name='descargas_list'),
]