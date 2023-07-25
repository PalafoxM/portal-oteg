from django.urls import path
from .import views 
from .views import delete_user,edit_user,edit_user_pwd, UserListView, UserAndProfileCreateView, UserAndProfileUpdateView, ResetPasswordView, ChangePasswordView

app_name = 'logIn'

urlpatterns = [
    path('login_user', views.logInUser, name='login_user'),
    path('logout_user', views.logOutUser, name='logout'),
    path('register_user', views.register_user, name='register'),
    path('users_crud', views.users_crud, name='users_crud'),
    path('delete_user/<int:user_id>/', delete_user, name='delete_user'),
    path('edit_user/<int:user_id>/', edit_user, name='edit_user'),
    path('edit_user_pwd', edit_user_pwd, name='edit_user_pwd'),
    path('usuarios-list', UserListView.as_view(), name='usuarios-list'),
    path('usuario-perfil-create', UserAndProfileCreateView.as_view(), name='usuarios-perfil-create'),
    path('usuario-perfil-update/<int:pk>', UserAndProfileUpdateView.as_view(), name='usuarios-perfil-update'),
    path('reset/password/', ResetPasswordView.as_view(), name='reset_password'),
    path('change/password/<str:token>/', ChangePasswordView.as_view(), name='change_password')
]
