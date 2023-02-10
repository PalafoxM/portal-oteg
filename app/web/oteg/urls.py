from django.urls import path
from oteg import views

urlpatterns = [
    path('', views.oteg, name='home'),
]