from django.urls import path
from .import views

urlpatterns = [
    path('user_panel',views.user_panel,name='user_panel'),
]
