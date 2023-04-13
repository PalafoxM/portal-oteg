from django.urls import path
from back.views.colaboradores.views import *
from back.views.contenido.views import *
from back.views.otros.views import *
from back.views.usuarios.views import *
from back.views.inventario_hotelero_gto.views import *

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
    path('crear-evento/', EventoCreateView.as_view(), name='evento_create'),
    path('eventos/eliminar/<int:pk>/', EventoDeleteView.as_view(), name='evento_delete'),
    path('eventos/editar/<int:pk>/', EventoUpdateView.as_view(), name='evento_update'),

    #contenido -> noticias
    path('noticias/list', NoticiaListView.as_view(), name='noticias_list'),
    path('noticias/add', NoticiaCreateView.as_view(), name='noticia_create'),
    path('noticias/edit/<int:pk>/', NoticiaUpdateView.as_view(), name='noticia_update'),
    path('noticias/delete/<int:pk>/', NoticiaDeleteView.as_view(), name='noticia_delete'),
    
    # contenido -> places of interest
    path('alba/list', AlbaListView.as_view(), name='alba_list'),
    path('alba/add', AlbaCreateView.as_view(), name='alba_create'),
    path('alba/edit/<int:pk>/', AlbaUpdateView.as_view(), name='alba_update'),
    path('alba/delete/<int:pk>/', AlbaDeleteView.as_view(), name='alba_delete'),
    # otros
    path('centrodocumental/list', centro_documental, name='centrodocumental'),
    path('addcategoria', add_seccion_centro_documental, name='addseccion'),
    path('delete-seccion/<int:seccion_id>/', delete_seccion, name='delete_seccion'),
    path('edit_-eccion/<int:seccion_id>/', edit_seccion, name='edit_seccion'),
    path('add-categoria/<int:seccion_id>/', add_categoria, name='add_categoria'),
    path('descargas/list', descargas_list, name='descargas_list'),
    # Usuarios
    path('usuarios/list', my_profile, name='profile'),
    #inventario_hotelero_gto
    path('inventario-hotelero-gto/list', InventarioHoteleroListView.as_view(), name='inventario_hotelero_list'),
    path('inventario-hotelero-gto/add', InventarioHoteleroCreateView.as_view(), name='inventario_hotelero_create'),
    path('inventario-hotelero-gto/edit/<int:pk>/', InventarioHoteleroUpdateView.as_view(), name='inventario_hotelero_update'),
    path('inventario-hotelero-gto/delete/<int:pk>/', InventarioHoteleroDeleteView.as_view(), name='inventario_hotelero_delete'),
    path('inventario-hotelero-gto/carga-masiva', CargaMasivaView.as_view(), name='inventario_hotelero_carga_masiva'),
]