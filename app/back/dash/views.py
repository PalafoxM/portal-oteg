from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group

# Create your views here.


@login_required(login_url='login')
def dash(request):
    username = request.user.username
    groups = Group.objects.filter(user=request.user)
    
    context = {

        "username": username,
        "groups": groups
    }

    return render(request, 'dash/dash.html', context)
