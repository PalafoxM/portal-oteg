from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.


@login_required(login_url='login')
def user_panel(req):
    username = req.user.username
    return render(req, 'users/panel.html', {"username": username})


@login_required(login_url='login')
def my_profile(req):
    username = req.user.username
    return render(req, 'users/profile.html', {"username": username})


