from django.urls import path
from back.views.colaboradores.views import *
from back.views.contenido.views import *
from back.views.otros.views import *
from back.views.usuarios.views import *
from back.views.fuente_info_datatur.views import *
from back.views.fuente_info_gasto_derrama.views import *
from back.views.fuente_info_otros_anuales.views import *

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
    path('crear_evento/', EventoCreateView.as_view(), name='evento_create'),
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
    path('centrodocumental/list', CentroDocumentalView.as_view(), name='centrodocumental'),
    path('add_section', SeccionCentroDocumentalCreate.as_view(), name='centrodocumenta_create'),

    path('delete_seccion/<int:pk>/', SeccionCentroDocumentalDelete.as_view(), name='CEDC_delete'),
    path('edit_seccion/<int:pk>/', SeccionCentroDocumentalUpdate.as_view(), name='CEDC_update'),
    path('get_sections',get_sections, name='get_sections'),


    #categorias de centro documental
    path('categorias/<int:pk>/', CategoriasListView.as_view(), name='categorias_list'),
    path('add_categoria/<int:pk>/', CategoriasCreateView.as_view() , name='add_categoria'),
    path('delete_categoria/<int:seccion_pk>/<int:pk>/', CategoriasDeleteView.as_view(), name='categoria_delete'),
    path('edit_categoria/<int:seccion_pk>/<int:pk>/', CategoriasUpdateView.as_view(), name='categoria_update'),
    path('descargas/list',DescargasView.as_view(), name='descargas_list'),

    
    path('get_categories', get_categories, name='get_categories'),

    #Glosario
    path('glosario/list', GlosarioListView.as_view(), name='glosario_list'),
    path('glosario/add', GlosarioCreateView.as_view(), name='glosario_create'),
    path('glosario/edit/<int:pk>/', GlosarioUpdateView.as_view(), name='glosario_updateg'),
    path('glosario/delete/<int:pk>/', GlosarioDeleteView.as_view(), name='glosario_delete'),

    # Barometro
    path('barometro/list', BarometroListView.as_view(), name='barometro_list'),
    path('barometro/add', BarometroCreateView.as_view(), name='barometro_create'),
    path('barometro/edit/<int:pk>/', BarometroUpdateView.as_view(), name='barometro_update'),
    path('barometro/delete/<int:pk>/', BarometroDeleteView.as_view(), name='barometro_delete'),


    #Fuentes de informacion DataTur
    path('fuentes_info/datatur', FuenteInfoDatatur.as_view(), name='fuente_info_datatour'),
    path('fuentes_info/datatur/add', FuenteInfoDataturCreate.as_view(), name='fuente_info_datatour_create'),
    path('fuentes_info/datatur/edit/<int:pk>/', FuenteInfoDataturUpdate.as_view(), name='fuente_info_datatour_update'),
    path('fuentes_info/datatur/delete/<int:pk>/', FuenteInfoDataturDelete.as_view(), name='fuente_info_datatour_delete'),
    path('upload_file', upload_file, name='upload_file2'),
    #Fuentes de informacion Gasto Derrama
    path('fuentes_info/gasto_derrama', FuenteInfoGastoDerrama.as_view(), name='fuente_info_gasto_derrama'),
    path('fuentes_info/gasto_derrama/add', FuenteInfoGastoDerramaCreate.as_view(), name='fuente_info_gasto_derrama_create'),
    path('fuentes_info/gasto_derrama/edit/<int:pk>/', FuenteInfoGastoDerramaUpdate.as_view(), name='fuente_info_gasto_derrama_update'),
    path('fuentes_info/gasto_derrama/delete/<int:pk>/', FuenteInfoGastoDerramaDelete.as_view(), name='fuente_info_gasto_derrama_delete'),

    #Fuentes de informacion Otros Anuales
    path('fuentes_info/otros_anuales', FuenteInfoOtrosAnuales.as_view(), name='fuente_info_otros_anuales'),
    path('fuentes_info/otros_anuales/add', FuenteInfoOtrosAnualesCreate.as_view(), name='fuente_info_otros_anuales_create'),
    path('fuentes_info/otros_anuales/edit/<int:pk>/', FuenteInfoOtrosAnualesUpdate.as_view(), name='fuente_info_otros_anuales_update'),
    path('fuentes_info/otros_anuales/delete/<int:pk>/', FuenteInfoOtrosAnualesDelete.as_view(), name='fuente_info_otros_anuales_delete'),
    
    path('usuarios/list', my_profile, name='profile'),

]