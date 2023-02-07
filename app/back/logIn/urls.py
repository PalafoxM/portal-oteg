from django.urls import path
from .import views 
from .views import delete_user
from .views import edit_user

urlpatterns = [
    path('login_user', views.logInUser, name='login'),
    path('logout_user', views.logOutUser, name='logout'),
    path('register_user', views.register_user, name='register'),
    path('users_crud', views.users_crud, name='users_crud'),
    path('delete_user/<int:user_id>/', delete_user, name='delete_user'),
    path('edit_user/<int:user_id>/', edit_user, name='edit_user'),
]
