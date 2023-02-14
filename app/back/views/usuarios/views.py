from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.



@login_required(login_url='login')
def my_profile(req):
    username = req.user.username
    context = {
        'username': username,
    }
    print(username + " lklkl")
    return render(req, 'back/users/porfile.html', context)


