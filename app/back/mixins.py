from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.http import Http404
from django.shortcuts import render


class SuperAdminOrAdminMixin(UserPassesTestMixin):
    def test_func(self):
        user = self.request.user
        return user.is_authenticated and (user.groups.filter(name='Super-Admin').exists() or user.groups.filter(name='Admin').exists()) and not user.groups.filter(name='Colaborador').exists()

    def handle_no_permission(self):
        return render(self.request, 'back/components/404.html', status=404)


class LoginRequiredMixin(UserPassesTestMixin):
    login_url = reverse_lazy('auth:login_user')

    def test_func(self):
        return self.request.user.is_authenticated

    def handle_no_permission(self):
        return redirect(self.login_url)

class SuperAdminMixin(UserPassesTestMixin):
    def test_func(self):
        user = self.request.user
        return user.is_authenticated and (user.groups.filter(name='Super-Admin').exists())

    def handle_no_permission(self):
        return render(self.request, 'back/components/404.html', status=404)

def test_func(self):
    user = self.request.user
    return user.is_authenticated and (user.groups.filter(name='Super-Admin').exists() or user.groups.filter(name='Admin').exists()) and not user.groups.filter(name='Colaborador').exists()
