from django.urls import path
from .import views

urlpatterns = [
    path('centrodocumental', views.centro_documental, name='centrodocumental'),
    path('addcategoria', views.add_seccion_centro_documental, name='addseccion'),
    path('delete_seccion/<int:seccion_id>/', views.delete_seccion, name='delete_seccion'),
    path('edit_seccion/<int:seccion_id>/', views.edit_seccion, name='edit_seccion'),
    path('add_categoria/<int:seccion_id>/', views.add_categoria, name='add_categoria'),
    
    ]


