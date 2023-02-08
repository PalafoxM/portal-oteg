from django.urls import path
from contenido.views import *

urlpatterns = [
    path('banner/lista', baners_list, name='banner_list'),
    path('banner/add', BannerCreateView.as_view(), name='banner_create'),
    path('banner/edit/<int:pk>/', BannerUpdateView.as_view(), name='banner_update'),
    path('banner/delete/<int:pk>/', BanneDeleteView.as_view(), name='banner_delete'),
]