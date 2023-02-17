from django.urls import path
from back.views.colaboradores.views import *
from back.views.contenido.views import *
from back.views.otros.views import *
from back.views.usuarios.views import *

app_name = 'dashboard'

urlpatterns = [
    path('publicaciones/list', PublicationsListView.as_view(), name='publicacion_list'),
    path('publicaciones/add', PublicationsCreateView.as_view(), name='publicacion_create'),
    path('publicaciones/edit/<int:pk>/', PublicationUpdateView.as_view(), name='publicacion_update'),
    path('publicaciones/delete/<int:pk>/', PublicationDeleteView.as_view(), name='publicacion_delete'),
    # contenido -> banner
    path('banner/list', BannerListView.as_view(), name='banner_list'),
    path('banner/add', BannerCreateView.as_view(), name='banner_create'),
    path('banner/edit/<int:pk>/', BannerUpdateView.as_view(), name='banner_update'),
    path('banner/delete/<int:pk>/', BanneDeleteView.as_view(), name='banner_delete'),
    # contenido -> places of interest
    path('place-of-interest/list', PlaceListView.as_view(), name='place_list'),
    path('place-of-interest/add', PlaceCreateView.as_view(), name='place_create'),
    path('place-of-interest/edit/<int:pk>/', PlaceUpdateView.as_view(), name='place_update'),
    path('place-of-interest/delete/<int:pk>/', PlaceDeleteView.as_view(), name='place_delete'),
    # contenido -> eventos
    path('eventos/list', EventoListView.as_view(), name='eventos_list'),
    #contenido -> noticias
    path('noticias/list', NoticiaListView.as_view(), name='noticias_list'),
    path('noticias/add', NoticiaCreateView.as_view(), name='noticia_create'),
    # otros
    path('centrodocumental/list', centro_documental, name='centrodocumental'),
    path('addcategoria', add_seccion_centro_documental, name='addseccion'),
    path('delete_seccion/<int:seccion_id>/', delete_seccion, name='delete_seccion'),
    path('edit_seccion/<int:seccion_id>/', edit_seccion, name='edit_seccion'),
    path('add_categoria/<int:seccion_id>/', add_categoria, name='add_categoria'),
    path('descargas/list', descargas_list, name='descargas_list'),
    # Usuarios
    path('usuarios/list', my_profile, name='profile'),
]