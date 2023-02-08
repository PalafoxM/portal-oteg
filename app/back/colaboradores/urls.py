from django.urls import path
from colaboradores.views import *
from contenido.views import *

app_name = 'colaboradores'

urlpatterns = [
    path('publicaciones/lista', publicaciones_list, name='publicacion_list'),
    path('publicaciones/add', PublicationsCreateView.as_view(), name='publicacion_create'),
    path('publicaciones/edit/<int:pk>/', PublicationUpdateView.as_view(), name='publicacion_update'),
    path('publicaciones/delete/<int:pk>/', PublicationDeleteView.as_view(), name='publicacion_delete'),
    # contenido
    path('banner/lista', baners_list, name='banner_list'),
    path('banner/add', BannerCreateView.as_view(), name='banner_create'),
    path('banner/edit/<int:pk>/', BannerUpdateView.as_view(), name='banner_update'),
    path('banner/delete/<int:pk>/', BanneDeleteView.as_view(), name='banner_delete'),
]