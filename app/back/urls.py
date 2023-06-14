from django.urls import path
from back.views.colaboradores.views import *
from back.views.contenido.views import *
from back.views.otros.views import *
from back.views.usuarios.views import *
from back.views.fuente_info_datatur.views import *
from back.views.fuente_info_gasto_derrama.views import *
from back.views.fuente_info_otros_anuales.views import *
from back.views.fuente_info_zonas_arq.views import *
from back.views.inventario_hotelero_gto.views import *
from back.views.inversion_publica.views import *
from back.views.inventario_hotelero_ent_nac.views import *
from back.views.calidad_aire.views import *
from back.views.fuente_informacion.view import *
from back.views.fuente_info_sensibilizacion.views import *
from back.views.utils.views import *
from back.views.catalago_categoria.views import *
from back.views.catalogo_segmentos.views import *
from back.views.catalogo_tipo_visitante.views import *
from back.views.catalogo_za_museos.views import *
from back.views.catalogo_destinos.views import *
from back.views.catalogo_destinos_aeropuerto.views import *
from back.views.proyectos_inversion.views import *
from back.views.fuente_info_certificacion.views import *
from back.views.fuente_info_invesion_priv.views import *
from back.views.fuente_info_empleo.views import *
from back.views.fuente_info_modelo_gd.views import *
from back.views.modulo_config.views import *
from back.views.modulo_config_destinos.views import *
from back.views.fuente_info_airbnb.views import *
from back.views.fuente_info_discapacidad.views import *
from back.views.fuente_info_segmentos.views import *
from back.views.fuente_info_aeropuertos.views import *
from back.views.fuente_info_aerolinea.views import *
from back.views.fuente_info_origen.views import *
from back.views.fuente_info_perfil_visitante_eventos.views import *
from back.views.fuente_info_entorno_nacional.views import *
from back.views.fuente_info_inventario_turistico.views import *
from back.views.fuente_info_directorio_hotelero.views import *
from back.views.fuente_info_perfil_visitante_destinos.views import *
from back.views.fuente_info_dt_agencias_de_viajes.views import *
from back.views.fuente_info_dt_alimentos_y_bebidas.views import *
from back.views.fuente_info_dt_arrendadoras.views import *
from back.views.fuente_info_dt_atractivos_recreacion_y_deporte.views import *
from back.views.fuente_info_dt_auxilio_turistico.views import *
from back.views.fuente_info_dt_balnearios_parques_acuaticos.views import *
from back.views.fuente_info_dt_campo_de_golf.views import *
from back.views.fuente_info_dt_capacitacion_turistica.views import *
from back.views.fuente_info_dt_guias_de_turistas.views import *
from back.views.fuente_info_dt_operadores.views import *
from back.views.fuente_info_dt_productos_turisticos.views import *
from back.views.fuente_info_dt_recintos_auditorios_y_salones.views import *
from back.views.fuente_info_dt_spa.views import *
from back.views.fuente_info_pasajeros_ent_nac.views import *


from django.conf import settings
from django.conf.urls.static import static

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
    path('fuentes_info/datatur/carga-masiva', DataturCargaMasivaView.as_view(), name='fuente_info_datatour_carga_masiva'),
    path('fuentes_info/datatur/descargar-archivo', DescargarArchivoDataturView.as_view(), name='fuente_info_datatour_descargar_archivo'),
    #Fuentes de informacion Gasto Derrama
    path('fuentes_info/gasto_derrama', FuenteInfoGastoDerrama.as_view(), name='fuente_info_gasto_derrama'),
    path('fuentes_info/gasto_derrama/add', FuenteInfoGastoDerramaCreate.as_view(), name='fuente_info_gasto_derrama_create'),
    path('fuentes_info/gasto_derrama/edit/<int:pk>/', FuenteInfoGastoDerramaUpdate.as_view(), name='fuente_info_gasto_derrama_update'),
    path('fuentes_info/gasto_derrama/delete/<int:pk>/', FuenteInfoGastoDerramaDelete.as_view(), name='fuente_info_gasto_derrama_delete'),
    path('fuentes_info/gasto-derrama/carga-masiva', GastoDerramaCargaMasivaView.as_view(), name='fuente_gasto_derrama_carga_masiva'),
    path('fuentes_info/gasto-derrama/descargar-archivo', GastoDerramaDescargarArchivoView.as_view(), name='fuente_gasto_derrama_descargar_archivo'),

    #Fuentes de informacion Otros Anuales
    path('fuentes_info/otros_anuales', FuenteInfoOtrosAnuales.as_view(), name='fuente_info_otros_anuales'),
    path('fuentes_info/otros_anuales/add', FuenteInfoOtrosAnualesCreate.as_view(), name='fuente_info_otros_anuales_create'),
    path('fuentes_info/otros_anuales/edit/<int:pk>/', FuenteInfoOtrosAnualesUpdate.as_view(), name='fuente_info_otros_anuales_update'),
    path('fuentes_info/otros_anuales/delete/<int:pk>/', FuenteInfoOtrosAnualesDelete.as_view(), name='fuente_info_otros_anuales_delete'),
    path('fuentes_info/otros-anuales/carga-masiva', OtrosAnualesCargaMasivaView.as_view(), name='fuente_otros_anuales_carga_masiva'),
    path('fuentes_info/otros-anuales/descargar-archivo', OtrosAnualeDescargarArchivoView.as_view(), name='fuente_otros_anuales_descargar_archivo'),
    
    #Fuentes de informacion Zonas Arqueologicas
    path('fuentes_info/zonas_arqueologicas', FuenteInfoZonasArqueologicas.as_view(), name='fuente_info_zonas_arqueologicas'),
    path('fuentes_info/zonas_arqueologicas/add', FuenteInfoZonasArqueologicasCreate.as_view(), name='fuente_info_zonas_arqueologicas_create'),
    path('fuentes_info/zonas_arqueologicas/edit/<int:pk>/', FuenteInfoZonasArqueologicasUpdate.as_view(), name='fuente_info_zonas_arqueologicas_update'),
    path('fuentes_info/zonas_arqueologicas/delete/<int:pk>/', FuenteInfoZonasArqueologicasDelete.as_view(), name='fuente_info_zonas_arqueologicas_delete'),
    path('fuentes_info/zonas-arqueologicas/carga-masiva', ZonasArqueoCargaMasivaView.as_view(), name='fuente_zonas_arqueologicas_carga_masiva'),
    path('fuentes_info/zonas-arqueologicas/descargar-archivo', ZonasArqueoDescargarArchivoView.as_view(), name='fuente_zonas_arqueologicas_descargar_archivo'),
    path('usuarios/list', my_profile, name='profile'),
    # Fuentes de informacion Sensibilizacion
    path('fuentes_info/sensibilizacion', FuenteInfoSensivilizacion.as_view(), name='fuente_info_sensibilizacion'),
    path('fuentes_info/sensibilizacion/add', FuenteInfoSensivilizacionCreate.as_view(), name='fuente_info_sensibilizacion_create'),
    path('fuentes_info/sensibilizacion/edit/<int:pk>/', FuenteInfoSensivilizacionUpdate.as_view(), name='fuente_info_sensibilizacion_update'),
    path('fuentes_info/sensibilizacion/delete/<int:pk>/', FuenteInfoSensivilizacionDelete.as_view(), name='fuente_info_sensibilizacion_delete'),
    path('fuentes_info/sensibilizacion/carga-masiva', SensivilizacionCargaMasivaView.as_view(), name='fuente_info_sensibilizacion_carga_masiva'),
    path('fuentes_info/sensibilizacion/descargar-archivo', SensivilizacionDescargarArchivoView.as_view(), name='fuente_info_sensibilizacion_descargar_archivo'),
    path('descargas/list', descargas_list, name='descargas_list'),
    #Fuentes info Certificacion 
    path('fuentes_info/certificacion', FuenteInfoCertificacion.as_view(), name='fuente_info_certificacion'),
    path('fuentes_info/certificacion/add', FuenteInfoCertificacionCreate.as_view(), name='fuente_info_certificacion_create'),
    path('fuentes_info/certificacion/edit/<int:pk>/', FuenteInfoCertificacionUpdate.as_view(), name='fuente_info_certificacion_update'),
    path('fuentes_info/certificacion/delete/<int:pk>/', FuenteInfoCertificacionDelete.as_view(), name='fuente_info_certificacion_delete'),
    path('fuentes_info/certificacion/carga-masiva', CertificacionCargaMasivaView.as_view(), name='fuente_info_certificacion_carga_masiva'),
    path('fuentes_info/certificacion/descargar-archivo', CertificacionDescargarArchivoView.as_view(), name='fuente_info_certificacion_descargar_archivo'),

    #Fuentes info Inversion Privada

    path('fuentes_info/inversion_privada', FuenteInfoInversionPriv.as_view(), name='fuente_info_inversion_privada'),
    path('fuentes_info/inversion_privada/add', FuenteInfoInversionPrivCreate.as_view(), name='fuente_info_inversion_privada_create'),
    path('fuentes_info/inversion_privada/edit/<int:pk>/', FuenteInfoInversionPrivUpdate.as_view(), name='fuente_info_inversion_privada_update'),
    path('fuentes_info/inversion_privada/delete/<int:pk>/', FuenteInfoInversionPrivDelete.as_view(), name='fuente_info_inversion_privada_delete'),
    path('fuentes_info/inversion_privada/get_p',get_inversion_privada, name='get_inversion_privada'),
    path('fuentes_info/inversion-privada/carga-masiva', InversionPrivCargaMasivaView.as_view(), name='fuente_info_inversion_privada_carga_masiva'),
    path('fuentes_info/inversion-privada/descargar-archivo', InversionPrivDescargarArchivoView.as_view(), name='fuente_info_inversion_privada_descargar_archivo'),

    # Fuentes info Modelo GD
    path('fuentes_info/modelo_gd', FuenteInfoModeloGD.as_view(), name='fuente_info_modelo_gd'),
    path('fuentes_info/modelo_gd/add', FuenteInfoModeloGDCreate.as_view(), name='fuente_info_modelo_gd_create'),
    path('fuentes_info/modelo_gd/edit/<int:pk>/', FuenteInfoModeloGDUpdate.as_view(), name='fuente_info_modelo_gd_update'),
    path('fuentes_info/modelo_gd/delete/<int:pk>/', FuenteInfoModeloGDDelete.as_view(), name='fuente_info_modelo_gd_delete'),


    #fuentes info empleo
    path('fuentes_info/empleo', FuenteInfoEmpleo.as_view(), name='fuente_info_empleo'),
    path('fuentes_info/empleo/add', FuenteInfoEmpleoCreate.as_view(), name='fuente_info_empleo_create'),
    path('fuentes_info/empleo/edit/<int:pk>/', FuenteInfoEmpleoUpdate.as_view(), name='fuente_info_empleo_update'),
    path('fuentes_info/empleo/delete/<int:pk>/', FuenteInfoEmpleoDelete.as_view(), name='fuente_info_empleo_delete'),
    path('fuentes_info/empleo/carga-masiva', EmpleoCargaMasivaView.as_view(), name='fuente_info_empleo_carga_masiva'),
    path('fuentes_info/empleo/descargar-archivo', EmpleoDescargarArchivoView.as_view(), name='fuente_info_empleo_descargar_archivo'),

    #fuente info airbnb
    path('fuentes_info/airbnb', FuenteInfoAirbnb.as_view(), name='fuente_info_airbnb'),
    path('fuentes_info/airbnb/add', FuenteInfoAirbnbCreate.as_view(), name='fuente_info_airbnb_create'),
    path('fuentes_info/airbnb/edit/<int:pk>/', FuenteInfoAirbnbUpdate.as_view(), name='fuente_info_airbnb_update'),
    path('fuentes_info/airbnb/delete/<int:pk>/', FuenteInfoAirbnbDelete.as_view(), name='fuente_info_airbnb_delete'),
    path('fuentes_info/airbnb/carga-masiva', AirbnbCargaMasivaView.as_view(), name='fuente_info_airbnb_carga_masiva'),
    path('fuentes_info/airbnb/descargar-archivo', AirbnbDescargarArchivoView.as_view(), name='fuente_info_airbnb_descargar_archivo'),


    
    # Usuarios
    path('usuarios/list', my_profile, name='profile'),
   
    #inventario_hotelero_gto
    path('inventario-hotelero-gto/list', InventarioHoteleroListView.as_view(), name='inventario_hotelero_list'),
    path('inventario-hotelero-gto/add', InventarioHoteleroCreateView.as_view(), name='inventario_hotelero_create'),
    path('inventario-hotelero-gto/edit/<int:pk>/', InventarioHoteleroUpdateView.as_view(), name='inventario_hotelero_update'),
    path('inventario-hotelero-gto/delete/<int:pk>/', InventarioHoteleroDeleteView.as_view(), name='inventario_hotelero_delete'),
    path('inventario-hotelero-gto/carga-masiva', CargaMasivaView.as_view(), name='inventario_hotelero_carga_masiva'),
    path('inventario-hotelero-gto/descargar-archivo', DescargarArchivoGTOView.as_view(), name='descargar_archivo_gto'),
    
    #inversion_publica
    path('inversion-publica/list', InversionPublicaListView.as_view(), name='inversion_publica_list'),
    path('inversion-publica/add', InversionPublicaCreateView.as_view(), name='inversion_publica_create'),
    path('inversion-publica/edit/<int:pk>/', InversionPublicaUpdateView.as_view(), name='inversion_publica_update'),
    path('inversion-publica/delete/<int:pk>/', InversionPublicaDeleteView.as_view(), name='inversion_publica_delete'),
    path('inversion-publica/carga-masiva', InversionPublicaCargaMasivaView.as_view(), name='inversion_publica_carga_masiva'),
    path('inventario-hotelero-ent-nac/descargar-archivo', DescargarArchivoInversionPublicaView.as_view(), name='descargar_archivo_inversion_publica'),
   
    #inventario_hotelero_ent_nac
    path('inventario-hotelero-ent-nac/list', InventarioHoteleroEntNacListView.as_view(), name='inventario_hotelero_ent_nac_list'),
    path('inventario-hotelero-ent-nac/add', InventarioHoteleroEntNacCreateView.as_view(), name='inventario_hotelero_ent_nac_create'),
    path('inventario-hotelero-ent-nac/edit/<int:pk>/', InventarioHoteleroEntNacUpdateView.as_view(), name='inventario_hotelero_ent_nac_update'),
    path('inventario-hotelero-ent-nac/delete/<int:pk>/', InventarioHoteleroEntNacDeleteView.as_view(), name='inventario_hotelero_ent_nac_delete'),
    path('inventario-hotelero-ent-nac/carga-masiva', InventarioHoteleroEntNacCargaMasivaView.as_view(), name='inventario_hotelero_ent_nac_carga_masiva'),
    path('inventario-hotelero-ent-nac/descargar-archivo', DescargarArchivoView.as_view(), name='descargar_archivo'),

    #calidad_aire
    path('calidad-aire/list', CalidadAireListView.as_view(), name='calidad_aire_list'),
    path('calidad-aire/add', CalidadAireCreateView.as_view(), name='calidad_aire_create'),
    path('calidad-aire/edit/<int:pk>/', CalidadAireUpdateView.as_view(), name='calidad_aire_update'),
    path('calidad-aire/delete/<int:pk>/', CalidadAireDeleteView.as_view(), name='calidad_aire_delete'),
    path('calidad-aire/carga-masiva', CalidadAireCargaMasivaView.as_view(), name='calidad_aire_carga_masiva'),
    path('calidad-aire/descargar-archivo', DescargarArchivoAireView.as_view(), name='descargar_archivo_aire'),


    # fuentes de informacion list
    path('fuente-informacion', FuentesInfoView.as_view(), name='fuente_informacion'),
    # Configuration list 
    path ('configuracion', ConfigurationView.as_view(), name='configuracion'),
    # utils
    #Typeahead Destinos
    path('typeahead/destinos', search_destinos, name='search_destinos'),
    #Typeahead Categorias
    path('typeahead/categorias', search_categorias, name='search_categorias'),
    #Typeahead Nombre ZA
    path('typeahead/nombre-za', search_nombre_za, name='search_nombre_za'),
    #Typeahead  entidades
    path('typeahead/entidades', search_entidades, name='search_entidades'),

    #Typeahead Destinos Aeropuerto
    path('typeahead/destinos-aeropuerto', search_destino_aeropuerto, name='search_destino_aeropuerto'),

    #Typeahead ID Destinos Aeropuerto
    path('typeahead/id-destinos-aeropuerto', search_id_destino_aeropuerto, name='search_id_destino_aeropuerto'),

    #Typeahead ID  Aeropuertoa
    path('typeahead/aeropuerto', search_aeropuerto, name='search_aeropuerto'),

    #Typeahead entidad aeropuerto

    path('typeahead/entidad-aeropuerto', search_entidad_aeropuerto, name='search_entidad_aeropuerto'),


    #catalago_categoria 
    path('catalago-categoria/list', CatalagoCategoriaListView.as_view(), name='catalago_categoria_list'),
    path('catalago-categoria/add', CatalagoCategoriaCreateView.as_view(), name='catalago_categoria_create'),
    path('catalago-categoria/edit/<int:pk>/', CatalagoCategoriaUpdateView.as_view(), name='catalago_categoria_update'),
    path('catalago-categoria/delete/<int:pk>/', CatalagoCategoriaDeleteView.as_view(), name='catalago_categoria_delete'),

    #catalago_segmento
    path('catalago-segmento/list', CatalagoSegmentosListView.as_view(), name='catalago_segmento_list'),
    path('catalago-segmento/add', CatalagoSegmentosCreateView.as_view(), name='catalago_segmento_create'),
    path('catalago-segmento/edit/<int:pk>/', CatalagoSegmentosUpdateView.as_view(), name='catalago_segmento_update'),
    path('catalago-segmento/delete/<int:pk>/', CatalagoSegmentosDeleteView.as_view(), name='catalago_segmento_delete'),

    #catalago_tipo_visitante
    path('catalago-tipo-visitante/list', CatalagoTipoVisistanteListView.as_view(), name='catalago_tipo_visitante_list'),
    path('catalago-tipo-visitante/add', CatalagoTipoVisistanteCreateView.as_view(), name='catalago_tipo_visitante_create'),
    path('catalago-tipo-visitante/edit/<int:pk>/', CatalagoTipoVisistanteUpdateView.as_view(), name='catalago_tipo_visitante_update'),
    path('catalago-tipo-visitante/delete/<int:pk>/', CatalagoTipoVisistanteDeleteView.as_view(), name='catalago_tipo_visitante_delete'),

    #catalogo_za_museos
    path('catalago-za-museos/list', CatalagoZAMuseosListView.as_view(), name='catalogo_za_museos_list'),
    path('catalago-za-museos/add', CatalagoZAMuseosCreateView.as_view(), name='catalogo_za_museos_create'),
    path('catalago-za-museos/edit/<int:pk>/', CatalagoZAMuseosUpdateView.as_view(), name='catalogo_za_museos_update'),
    path('catalago-za-museos/delete/<int:pk>/', CatalagoZAMuseosDeleteView.as_view(), name='catalogo_za_museos_delete'),

    #catalogo_destinos
    path('catalago-destinos/list', CatalagoDestinoListView.as_view(), name='catalogo_destinos_list'),
    path('catalago-destinos/add', CatalagoDestinoCreateView.as_view(), name='catalogo_destinos_create'),
    path('catalago-destinos/edit/<int:pk>/', CatalagoDestinoUpdateView.as_view(), name='catalogo_destinos_update'),
    path('catalago-destinos/delete/<int:pk>/', CatalagoDestinoDeleteView.as_view(), name='catalogo_destinos_delete'),

    #catalogo_destinos_aeropuerto
    path('catalago-destinos-aeropuerto/list', CatalagoDestinoAeropuertoListView.as_view(), name='catalogo_destinos_aeropuerto_list'),
    path('catalago-destinos-aeropuerto/add', CatalagoDestinoAeropuertoCreateView.as_view(), name='catalogo_destinos_aeropuerto_create'),
    path('catalago-destinos-aeropuerto/edit/<int:pk>/', CatalagoDestinoAeropuertoUpdateView.as_view(), name='catalogo_aeropuerto_destinos_update'),
    path('catalago-destinos-aeropuerto/delete/<int:pk>/', CatalagoDestinoAeropuertoDeleteView.as_view(), name='catalogo_destinos_aeropuerto_delete'),

    #proyectos_inversion
    path('proyectos-inversion/list', ProyectoInversionListView.as_view(), name='proyectos_inversion_list'),
    path('proyectos-inversion/add', ProyectoInversionCreateView.as_view(), name='proyectos_inversion_create'),
    path('proyectos-inversion/edit/<int:pk>/', ProyectoInversionUpdateView.as_view(), name='proyectos_inversion_update'),
    path('proyectos-inversion/delete/<int:pk>/', ProyectoInversionDeleteView.as_view(), name='proyectos_inversion_delete'),

    #modlulos configuracion
    
    #modlulo Configuracion DEstinos 
    path('configuracion-destinos/list', ModiuloConfigDestinos.as_view(), name='configuracion_destinos_list'),
    path('configuracion-destinos/add', ModiuloConfigDestinosCreateView.as_view(), name='configuracion_destinos_create'),
    path('configuracion-destinos/edit/<int:pk>/', ModiuloConfigDestinosUpdateView.as_view(), name='configuracion_destinos_update'),
    path('configuracion-destinos/delete/<int:pk>/', ModiuloConfigDestinosDeleteView.as_view(), name='configuracion_destinos_delete'),
    #fuentes info discapacidad
    path('fuentes-info/discapacidad', FuenteInfoDiscapacidad.as_view(), name='fuente_info_discapacidad'),
    path('fuentes-info/discapacidad/add', FuenteInfoDiscapacidadCreate.as_view(), name='fuente_info_discapacidad_create'),
    path('fuentes-info/discapacidad/edit/<int:pk>/', FuenteInfoDiscapacidadUpdate.as_view(), name='fuente_info_discapacidad_update'),
    path('fuentes-info/discapacidad/delete/<int:pk>/', FuenteInfoDiscapacidadDelete.as_view(), name='fuente_info_discapacidad_delete'),
    path('fuentes-info/discapacidad/carga-masiva', DiscapacidadCargaMasivaView.as_view(), name='fuente_info_discapacidad_carga_masiva'),
    path('fuentes-info/discapacidad/descargar-archivo', DiscapacidadDescargarArchivoView.as_view(), name='fuente_info_discapacidad_descargar_archivo'),
    
    #fuentes info %segmentos
    path('fuentes-info/segmentos', FuenteInfoParticipacionSegmentos.as_view(), name='fuente_info_segmentos'),
    path('fuentes-info/segmentos/add', FuenteInfoParticipacionSegmentosCreate.as_view(), name='fuente_info_segmentos_create'),
    path('fuentes-info/segmentos/edit/<int:pk>/', FuenteInfoParticipacionSegmentosUpdate.as_view(), name='fuente_info_segmentos_update'),
    path('fuentes-info/segmentos/delete/<int:pk>/', FuenteInfoParticipacionSegmentosDelete.as_view(), name='fuente_info_segmentos_delete'),
    path('fuentes-info/segmentos/carga-masiva', ParticipacionSegmentosCargaMasivaView.as_view(), name='fuente_info_segmentos_carga_masiva'),
    path('fuentes-info/segmentos/descargar-archivo', ParticipacionSegmentosDescargarArchivoView.as_view(), name='fuente_info_segmentos_descargar_archivo'),
    #fuentes inft %Origen
    path('fuentes-info/origen', FuenteInfoParticipacionOrigen.as_view(), name='fuente_info_origen'),
    path('fuentes-info/origen/add', FuenteInfoParticipacionOrigenCreate.as_view(), name='fuente_info_origen_create'),
    path('fuentes-info/origen/edit/<int:pk>/', FuenteInfoParticipacionOrigenUpdate.as_view(), name='fuente_info_origen_update'),
    path('fuentes-info/origen/delete/<int:pk>/', FuenteInfoParticipacionOrigenDelete.as_view(), name='fuente_info_origen_delete'),
    path('fuentes-info/origen/carga-masiva', OrigenCargaMasivaView.as_view(), name='fuente_info_origen_carga_masiva'),
    path('fuentes-info/origen/descargar-archivo', OrigenDescargarArchivoView.as_view(), name='fuente_info_origen_descargar_archivo'),
    
    #fuetes info perfil visitante eventos
    path('fuentes-info/perfil-visitante-eventos', FuenteInfoPerfilVisitanteEventos.as_view(), name='fuente_info_perfil_visitante_eventos'),
    path('fuentes-info/perfil-visitante-eventos/add', FuenteInfoPerfilVisitanteEventosCreate.as_view(), name='fuente_info_perfil_visitante_eventos_create'),
    path('fuentes-info/perfil-visitante-eventos/edit/<int:pk>/', FuenteInfoPerfilVisitanteEventosUpdate.as_view(), name='fuente_info_perfil_visitante_eventos_update'),
    path('fuentes-info/perfil-visitante-eventos/delete/<int:pk>/', FuenteInfoPerfilVisitanteEventosDelete.as_view(), name='fuente_info_perfil_visitante_eventos_delete'),
    path('fuentes-info/perfil-visitante-eventos/carga-masiva', PerfilVisitanteEventosCargaMasivaView.as_view(), name='fuente_info_perfil_visitante_eventos_carga_masiva'),
    path('fuentes-info/perfil-visitante-eventos/descargar-archivo', PerfilVisitanteEventosDescargarArchivoView.as_view(), name='fuente_info_perfil_visitante_eventos_descargar_archivo'),

    #fuetes info perfil visitante DEstinos
    path('fuentes-info/perfil-visitante-destinos', FuenteInfoPerfilVisitanteDestinos.as_view(), name='fuente_info_perfil_visitante_destinos'),
    path('fuentes-info/perfil-visitante-destinos/add', FuenteInfoPerfilVisitanteDestinosCreate.as_view(), name='fuente_info_perfil_visitante_destinos_create'),
    path('fuentes-info/perfil-visitante-destinos/edit/<int:pk>/', FuenteInfoPerfilVisitanteDestinosUpdate.as_view(), name='fuente_info_perfil_visitante_destinos_update'),
    path('fuentes-info/perfil-visitante-destinos/delete/<int:pk>/', FuenteInfoPerfilVisitanteDestinosDelete.as_view(), name='fuente_info_perfil_visitante_destinos_delete'),
    path('fuentes-info/perfil-visitante-destinos/carga-masiva', PerfilVisitanteDestinosCargaMasivaView.as_view(), name='fuente_info_perfil_visitante_destinos_carga_masiva'),
    path('fuentes-info/perfil-visitante-destinos/descargar-archivo', PerfilVisitanteDestinosDescargarArchivoView.as_view(), name='fuente_info_perfil_visitante_destinos_descargar_archivo'),

    #fuetes info entorno nacional
    path('fuentes-info/entorno-nacional', FuenteInfoEntornoNacional.as_view(), name='fuente_info_entorno_nacional'),
    path('fuentes-info/entorno-nacional/add', FuenteInfoEntornoNacionalCreate.as_view(), name='fuente_info_entorno_nacional_create'),
    path('fuentes-info/entorno-nacional/edit/<int:pk>/', FuenteInfoEntornoNacionalUpdate.as_view(), name='fuente_info_entorno_nacional_update'),
    path('fuentes-info/entorno-nacional/delete/<int:pk>/', FuenteInfoEntornoNacionalDelete.as_view(), name='fuente_info_entorno_nacional_delete'),
    path('fuentes-info/entorno-nacional/carga-masiva', EntornoNacionalCargaMasivaView.as_view(), name='fuente_info_entorno_nacional_carga_masiva'),
    path('fuentes-info/entorno-nacional/descargar-archivo', EntornoNacionalDescargarArchivoView.as_view(), name='fuente_info_entorno_nacional_descargar_archivo'),

    #fuentes info pasajeros_ent_nac
    path('fuentes-info/pasajeros-ent-nac', FuenteInfoPasajerosEntNacView.as_view(), name='fuente_info_pasajeros_ent_nac'),
    path('fuentes-info/pasajeros-ent-nac/add', FuenteInfoPasajerosEntNacCreate.as_view(), name='fuente_info_pasajeros_ent_nac_create'),
    path('fuentes-info/pasajeros-ent-nac/edit/<int:pk>/', FuenteInfoPasajerosEntNacUpdate.as_view(), name='fuente_info_pasajeros_ent_nac_update'),
    path('fuentes-info/pasajeros-ent-nac/delete/<int:pk>/', FuenteInfoPasajerosEntNacDelete.as_view(), name='fuente_info_pasajeros_ent_nac_delete'),
    path('fuentes-info/pasajeros-ent-nac/carga-masiva', PasajerosEntNacCargaMasivaView.as_view(), name='fuente_info_pasajeros_ent_nac_carga_masiva'),
    path('fuentes-info/pasajeros-ent-nac/descargar-archivo', PasajerosEntNacDescargarArchivoView.as_view(), name='fuente_info_pasajeros_ent_nac_descargar_archivo'),

    #fuentes info aeropuertos
    path('fuentes-info/aeropuertos', FuenteInfoAeropuerto.as_view(), name='fuente_info_aeropuertos'),
    path('fuentes-info/aeropuertos/add', FuenteInfoAeropuertoCreate.as_view(), name='fuente_info_aeropuertos_create'),
    path('fuentes-info/aeropuertos/edit/<int:pk>/', FuenteInfoAeropuertoUpdate.as_view(), name='fuente_info_aeropuertos_update'),
    path('fuentes-info/aeropuertos/delete/<int:pk>/', FuenteInfoAeropuertoDelete.as_view(), name='fuente_info_aeropuertos_delete'),
    path('fuentes-info/aeropuertos/carga-masiva', AeropuertoCargaMasivaView.as_view(), name='fuente_info_aeropuertos_carga_masiva'),
    path('fuentes-info/aeropuertos/descargar-archivo', AeropuertoDescargarArchivoView.as_view(), name='fuente_info_aeropuertos_descargar_archivo'),
    
    #fuentes info aerolineas
    path('fuentes-info/aerolineas', FuenteInfoAerolinea.as_view(), name='fuente_info_aerolineas'),
    path('fuentes-info/aerolineas/add', FuenteInfoAerolineaCreate.as_view(), name='fuente_info_aerolineas_create'),
    path('fuentes-info/aerolineas/edit/<int:pk>/', FuenteInfoAerolineaUpdate.as_view(), name='fuente_info_aerolineas_update'),
    path('fuentes-info/aerolineas/delete/<int:pk>/', FuenteInfoAerolineaDelete.as_view(), name='fuente_info_aerolineas_delete'),
    path('fuentes-info/aerolineas/carga-masiva', AerolineaCargaMasivaView.as_view(), name='fuente_info_aerolineas_carga_masiva'),
    path('fuentes-info/aerolineas/descargar-archivo', AerolineaDescargarArchivoView.as_view(), name='fuente_info_aerolineas_descargar_archivo'),
    
    #fuentes info inventario_turistico
    path('fuentes-info/inventario-turistico', FuenteInfoInventarioTuristico.as_view(), name='fuente_info_inventario_turistico'),
    path('fuentes-info/inventario-turistico/add', FuenteInfoInventarioTuristicoCreate.as_view(), name='fuente_info_inventario_turistico_create'),
    path('fuentes-info/inventario-turistico/edit/<int:pk>/', FuenteInfoInventarioTuristicoUpdate.as_view(), name='fuente_info_inventario_turistico_update'),
    path('fuentes-info/inventario-turistico/delete/<int:pk>/', FuenteInfoInventarioTuristicoDelete.as_view(), name='fuente_info_inventario_turistico_delete'),
    path('fuentes-info/inventario-turistico/carga-masiva', InventarioTuristicoCargaMasivaView.as_view(), name='fuente_info_inventario_turistico_carga_masiva'),
    path('fuentes-info/inventario-turistico/descargar-archivo', InventarioTuristicoDescargarArchivoView.as_view(), name='fuente_info_inventario_turistico_descargar_archivo'),
    
    #fuentes info directorio_hotelero
    path('fuentes-info/directorio-hotelero', FuenteInfoDirectorioHotelero.as_view(), name='fuente_info_directorio_hotelero'),
    path('fuentes-info/directorio-hotelero/add', FuenteInfoDirectorioHoteleroCreate.as_view(), name='fuente_info_directorio_hotelero_create'),
    path('fuentes-info/directorio-hotelero/edit/<int:pk>/', FuenteInfoDirectorioHoteleroUpdate.as_view(), name='fuente_info_directorio_hotelero_update'),
    path('fuentes-info/directorio-hotelero/delete/<int:pk>/', FuenteInfoDirectorioHoteleroDelete.as_view(), name='fuente_info_directorio_hotelero_delete'),
    path('fuentes-info/directorio-hotelero/carga-masiva', DirectorioHoteleroCargaMasivaView.as_view(), name='fuente_info_directorio_hotelero_carga_masiva'),
    path('fuentes-info/directorio-hotelero/descargar-archivo', DirectorioHoteleroDescargarArchivoView.as_view(), name='fuente_info_directorio_hotelero_descargar_archivo'),
    
    #fuentes info dt_agencias_de_viajes
    path('fuentes-info/dt-agencias-viajes', FuenteInfoDirectorioAgenciasDeViajes.as_view(), name='fuente_info_dt_agencias_de_viajes'),
    path('fuentes-info/dt-agencias-viajes/add', FuenteInfoDirectorioAgenciasDeViajesCreate.as_view(), name='fuente_info_dt_agencias_de_viajes_create'),
    path('fuentes-info/dt-agencias-viajes/edit/<int:pk>/', FuenteInfoDirectorioAgenciasDeViajesUpdate.as_view(), name='fuente_info_dt_agencias_de_viajes_update'),
    path('fuentes-info/dt-agencias-viajes/delete/<int:pk>/', FuenteInfoDirectorioAgenciasDeViajesDelete.as_view(), name='fuente_info_dt_agencias_de_viajes_delete'),
    path('fuentes-info/dt-agencias-viajes/carga-masiva', DirectorioAgenciasDeViajesCargaMasivaView.as_view(), name='fuente_info_dt_agencias_de_viajes_carga_masiva'),
    path('fuentes-info/dt-agencias-viajes/descargar-archivo', DirectorioAgenciasDeViajesDescargarArchivoView.as_view(), name='fuente_info_dt_agencias_de_viajes_descargar_archivo'),
    
    #fuentes info dt_alimentos_y_bebidas
    path('fuentes-info/dt-alimentos-bebidas', FuenteInfoDirectorioAlimentosYBebidas.as_view(), name='fuente_info_dt_alimentos_y_bebidas'),
    path('fuentes-info/dt-alimentos-bebidas/add', FuenteInfoDirectorioAlimentosYBebidasCreate.as_view(), name='fuente_info_dt_alimentos_y_bebidas_create'),
    path('fuentes-info/dt-alimentos-bebidas/edit/<int:pk>/', FuenteInfoDirectorioAlimentosYBebidasUpdate.as_view(), name='fuente_info_dt_alimentos_y_bebidas_update'),
    path('fuentes-info/dt-alimentos-bebidas/delete/<int:pk>/', FuenteInfoDirectorioAlimentosYBebidasDelete.as_view(), name='fuente_info_dt_alimentos_y_bebidas_delete'),
    path('fuentes-info/dt-alimentos-bebidas/carga-masiva', DirectorioAlimentosYBebidasCargaMasivaView.as_view(), name='fuente_info_dt_alimentos_y_bebidas_carga_masiva'),
    path('fuentes-info/dt-alimentos-bebidas/descargar-archivo', DirectorioAlimentosYBebidasDescargarArchivoView.as_view(), name='fuente_info_dt_alimentos_y_bebidas_descargar_archivo'),
    
    #fuentes info dt_arrendadoras
    path('fuentes-info/dt-arrendadoras', FuenteInfoDirectorioArrendadoras.as_view(), name='fuente_info_dt_arrendadoras'),
    path('fuentes-info/dt-arrendadoras/add', FuenteInfoDirectorioArrendadorasCreate.as_view(), name='fuente_info_dt_arrendadoras_create'),
    path('fuentes-info/dt-arrendadoras/edit/<int:pk>/', FuenteInfoDirectorioArrendadorasUpdate.as_view(), name='fuente_info_dt_arrendadoras_update'),
    path('fuentes-info/dt-arrendadoras/delete/<int:pk>/', FuenteInfoDirectorioArrendadorasDelete.as_view(), name='fuente_info_dt_arrendadoras_delete'),
    path('fuentes-info/dt-arrendadoras/carga-masiva', DirectorioArrendadorasCargaMasivaView.as_view(), name='fuente_info_dt_arrendadoras_carga_masiva'),
    path('fuentes-info/dt-arrendadoras/descargar-archivo', DirectorioArrendadorasDescargarArchivoView.as_view(), name='fuente_info_dt_arrendadoras_descargar_archivo'),
    
    #fuentes info dt_atractivos_recreacion_y_deporte
    path('fuentes-info/dt-atractivos-recreacion-deporte', FuenteInfoDirectorioActivosRecreacionYDeporte.as_view(), name='fuente_info_dt_atractivos_recreacion_y_deporte'),
    path('fuentes-info/dt-atractivos-recreacion-deporte/add', FuenteInfoDirectorioActivosRecreacionYDeporteCreate.as_view(), name='fuente_info_dt_atractivos_recreacion_y_deporte_create'),
    path('fuentes-info/dt-atractivos-recreacion-deporte/edit/<int:pk>/', FuenteInfoDirectorioActivosRecreacionYDeporteUpdate.as_view(), name='fuente_info_dt_atractivos_recreacion_y_deporte_update'),
    path('fuentes-info/dt-atractivos-recreacion-deporte/delete/<int:pk>/', FuenteInfoDirectorioActivosRecreacionYDeporteDelete.as_view(), name='fuente_info_dt_atractivos_recreacion_y_deporte_delete'),
    path('fuentes-info/dt-atractivos-recreacion-deporte/carga-masiva', DirectorioActivosRecreacionYDeporteCargaMasivaView.as_view(), name='fuente_info_dt_atractivos_recreacion_y_deporte_carga_masiva'),
    path('fuentes-info/dt-atractivos-recreacion-deporte/descargar-archivo', DirectorioActivosRecreacionYDeporteDescargarArchivoView.as_view(), name='fuente_info_dt_atractivos_recreacion_y_deporte_descargar_archivo'),
    
    #fuentes info dt_auxilio_turistico
    path('fuentes-info/dt-auxilio-turistico', FuenteInfoDirectorioAuxilioTuristico.as_view(), name='fuente_info_dt_auxilio_turistico'),
    path('fuentes-info/dt-auxilio-turistico/add', FuenteInfoDirectorioAuxilioTuristicoCreate.as_view(), name='fuente_info_dt_auxilio_turistico_create'),
    path('fuentes-info/dt-auxilio-turistico/edit/<int:pk>/', FuenteInfoDirectorioAuxilioTuristicoUpdate.as_view(), name='fuente_info_dt_auxilio_turistico_update'),
    path('fuentes-info/dt-auxilio-turistico/delete/<int:pk>/', FuenteInfoDirectorioAuxilioTuristicoDelete.as_view(), name='fuente_info_dt_auxilio_turistico_delete'),
    path('fuentes-info/dt-auxilio-turistico/carga-masiva', DirectorioAuxilioTuristicoCargaMasivaView.as_view(), name='fuente_info_dt_auxilio_turistico_carga_masiva'),
    path('fuentes-info/dt-auxilio-turistico/descargar-archivo', DirectorioAuxilioTuristicoDescargarArchivoView.as_view(), name='fuente_info_dt_auxilio_turistico_descargar_archivo'),
    
    #fuentes info dt_balnearios_parques_acuaticos
    path('fuentes-info/dt-balnearios-parques-acuaticos', FuenteInfoDirectorioBalneariosParquesAcuaticos.as_view(), name='fuente_info_dt_balnearios_parques_acuaticos'),
    path('fuentes-info/dt-balnearios-parques-acuaticos/add', FuenteInfoDirectorioBalneariosParquesAcuaticosCreate.as_view(), name='fuente_info_dt_balnearios_parques_acuaticos_create'),
    path('fuentes-info/dt-balnearios-parques-acuaticos/edit/<int:pk>/', FuenteInfoDirectorioBalneariosParquesAcuaticosUpdate.as_view(), name='fuente_info_dt_balnearios_parques_acuaticos_update'),
    path('fuentes-info/dt-balnearios-parques-acuaticos/delete/<int:pk>/', FuenteInfoDirectorioBalneariosParquesAcuaticosDelete.as_view(), name='fuente_info_dt_balnearios_parques_acuaticos_delete'),
    path('fuentes-info/dt-balnearios-parques-acuaticos/carga-masiva', DirectorioBalneariosParquesAcuaticosCargaMasivaView.as_view(), name='fuente_info_dt_balnearios_parques_acuaticos_carga_masiva'),
    path('fuentes-info/dt-balnearios-parques-acuaticos/descargar-archivo', DirectorioBalneariosParquesAcuaticosDescargarArchivoView.as_view(), name='fuente_info_dt_balnearios_parques_acuaticos_descargar_archivo'),
    
    #fuentes info dt_campo_de_golf
    path('fuentes-info/dt-campo-golf', FuenteInfoDirectorioCampoDeGolf.as_view(), name='fuente_info_dt_campo_de_golf'),
    path('fuentes-info/dt-campo-golf/add', FuenteInfoDirectorioCampoDeGolfCreate.as_view(), name='fuente_info_dt_campo_de_golf_create'),
    path('fuentes-info/dt-campo-golf/edit/<int:pk>/', FuenteInfoDirectorioCampoDeGolfUpdate.as_view(), name='fuente_info_dt_campo_de_golf_update'),
    path('fuentes-info/dt-campo-golf/delete/<int:pk>/', FuenteInfoDirectorioCampoDeGolfDelete.as_view(), name='fuente_info_dt_campo_de_golf_delete'),
    path('fuentes-info/dt-campo-golf/carga-masiva', DirectorioCampoDeGolfCargaMasivaView.as_view(), name='fuente_info_dt_campo_de_golf_carga_masiva'),
    path('fuentes-info/dt-campo-golf/descargar-archivo', DirectorioCampoDeGolfDescargarArchivoView.as_view(), name='fuente_info_dt_campo_de_golf_descargar_archivo'),
    
    #fuentes info dt_capacitacion_turistica
    path('fuentes-info/dt-capacitacion-turistica', FuenteInfoDirectorioCapacitacionTuristica.as_view(), name='fuente_info_dt_capacitacion_turistica'),
    path('fuentes-info/dt-capacitacion-turistica/add', FuenteInfoDirectorioCapacitacionTuristicaCreate.as_view(), name='fuente_info_dt_capacitacion_turistica_create'),
    path('fuentes-info/dt-capacitacion-turistica/edit/<int:pk>/', FuenteInfoDirectorioCapacitacionTuristicaUpdate.as_view(), name='fuente_info_dt_capacitacion_turistica_update'),
    path('fuentes-info/dt-capacitacion-turistica/delete/<int:pk>/', FuenteInfoDirectorioCapacitacionTuristicaDelete.as_view(), name='fuente_info_dt_capacitacion_turistica_delete'),
    path('fuentes-info/dt-capacitacion-turistica/carga-masiva', DirectorioCapacitacionTuristicaCargaMasivaView.as_view(), name='fuente_info_dt_capacitacion_turistica_carga_masiva'),
    path('fuentes-info/dt-capacitacion-turistica/descargar-archivo', DirectorioCapacitacionTuristicaDescargarArchivoView.as_view(), name='fuente_info_dt_capacitacion_turistica_descargar_archivo'),
    
    #fuentes info dt_guias_de_turistas
    path('fuentes-info/dt-guias-turistas', FuenteInfoDirectorioGuiasDeTuristas.as_view(), name='fuente_info_dt_guias_de_turistas'),
    path('fuentes-info/dt-guias-turistas/add', FuenteInfoDirectorioGuiasDeTuristasCreate.as_view(), name='fuente_info_dt_guias_de_turistas_create'),
    path('fuentes-info/dt-guias-turistas/edit/<int:pk>/', FuenteInfoDirectorioGuiasDeTuristasUpdate.as_view(), name='fuente_info_dt_guias_de_turistas_update'),
    path('fuentes-info/dt-guias-turistas/delete/<int:pk>/', FuenteInfoDirectorioGuiasDeTuristasDelete.as_view(), name='fuente_info_dt_guias_de_turistas_delete'),
    path('fuentes-info/dt-guias-turistas/carga-masiva', DirectorioGuiasDeTuristasCargaMasivaView.as_view(), name='fuente_info_dt_guias_de_turistas_carga_masiva'),
    path('fuentes-info/dt-guias-turistas/descargar-archivo', DirectorioGuiasDeTuristasDescargarArchivoView.as_view(), name='fuente_info_dt_guias_de_turistas_descargar_archivo'),
    
    #fuentes info dt_operadores
    path('fuentes-info/dt-operadores', FuenteInfoDirectorioOperadores.as_view(), name='fuente_info_dt_operadores'),
    path('fuentes-info/dt-operadores/add', FuenteInfoDirectorioOperadoresCreate.as_view(), name='fuente_info_dt_operadores_create'),
    path('fuentes-info/dt-operadores/edit/<int:pk>/', FuenteInfoDirectorioOperadoresUpdate.as_view(), name='fuente_info_dt_operadores_update'),
    path('fuentes-info/dt-operadores/delete/<int:pk>/', FuenteInfoDirectorioOperadoresDelete.as_view(), name='fuente_info_dt_operadores_delete'),
    path('fuentes-info/dt-operadores/carga-masiva', DirectorioOperadoresCargaMasivaView.as_view(), name='fuente_info_dt_operadores_carga_masiva'),
    path('fuentes-info/dt-operadores/descargar-archivo', DirectorioOperadoresDescargarArchivoView.as_view(), name='fuente_info_dt_operadores_descargar_archivo'),
    
    #fuentes info dt_productos_turisticos
    path('fuentes-info/dt-productos-turisticos', FuenteInfoDirectorioProductosTuristicos.as_view(), name='fuente_info_dt_productos_turisticos'),
    path('fuentes-info/dt-productos-turisticos/add', FuenteInfoDirectorioProductosTuristicosCreate.as_view(), name='fuente_info_dt_productos_turisticos_create'),
    path('fuentes-info/dt-productos-turisticos/edit/<int:pk>/', FuenteInfoDirectorioProductosTuristicosUpdate.as_view(), name='fuente_info_dt_productos_turisticos_update'),
    path('fuentes-info/dt-productos-turisticos/delete/<int:pk>/', FuenteInfoDirectorioProductosTuristicosDelete.as_view(), name='fuente_info_dt_productos_turisticos_delete'),
    path('fuentes-info/dt-productos-turisticos/carga-masiva', DirectorioProductosTuristicosCargaMasivaView.as_view(), name='fuente_info_dt_productos_turisticos_carga_masiva'),
    path('fuentes-info/dt-productos-turisticos/descargar-archivo', DirectorioProductosTuristicosDescargarArchivoView.as_view(), name='fuente_info_dt_productos_turisticos_descargar_archivo'),
    
    #fuentes info dt_recintos_auditorios_y_salones
    path('fuentes-info/dt-recintos-auditorios-salones', FuenteInfoDirectorioRecintosAuditoriosYSalones.as_view(), name='fuente_info_dt_recintos_auditorios_y_salones'),
    path('fuentes-info/dt-recintos-auditorios-salones/add', FuenteInfoDirectorioRecintosAuditoriosYSalonesCreate.as_view(), name='fuente_info_dt_recintos_auditorios_y_salones_create'),
    path('fuentes-info/dt-recintos-auditorios-salones/edit/<int:pk>/', FuenteInfoDirectorioRecintosAuditoriosYSalonesUpdate.as_view(), name='fuente_info_dt_recintos_auditorios_y_salones_update'),
    path('fuentes-info/dt-recintos-auditorios-salones/delete/<int:pk>/', FuenteInfoDirectorioRecintosAuditoriosYSalonesDelete.as_view(), name='fuente_info_dt_recintos_auditorios_y_salones_delete'),
    path('fuentes-info/dt-recintos-auditorios-salones/carga-masiva', DirectorioRecintosAuditoriosYSalonesCargaMasivaView.as_view(), name='fuente_info_dt_recintos_auditorios_y_salones_carga_masiva'),
    path('fuentes-info/dt-recintos-auditorios-salones/descargar-archivo', DirectorioRecintosAuditoriosYSalonesDescargarArchivoView.as_view(), name='fuente_info_dt_recintos_auditorios_y_salones_descargar_archivo'),
    
    #fuentes info dt_spa
    path('fuentes-info/dt-spa', FuenteInfoDirectorioSpa.as_view(), name='fuente_info_dt_spa'),
    path('fuentes-info/dt-spa/add', FuenteInfoDirectorioSpaCreate.as_view(), name='fuente_info_dt_spa_create'),
    path('fuentes-info/dt-spa/edit/<int:pk>/', FuenteInfoDirectorioSpaUpdate.as_view(), name='fuente_info_dt_spa_update'),
    path('fuentes-info/dt-spa/delete/<int:pk>/', FuenteInfoDirectorioSpaDelete.as_view(), name='fuente_info_dt_spa_delete'),
    path('fuentes-info/dt-spa/carga-masiva', DirectorioSpaCargaMasivaView.as_view(), name='fuente_info_dt_spa_carga_masiva'),
    path('fuentes-info/dt-spa/descargar-archivo', DirectorioSpaDescargarArchivoView.as_view(), name='fuente_info_dt_spa_descargar_archivo'),
    
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)