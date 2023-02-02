from django.urls import path
from .import views

urlpatterns = [
    path('login_user',views.logInUser,name='login'),
    path('logout_user',views.logOutUser,name='logout'),
    path('register_user',views.register_user,name='register'),
]
