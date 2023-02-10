from django.urls import path
from solicitudes import views

urlpatterns = [
    path('', views.solicitudes, name='solicitudes'),
]