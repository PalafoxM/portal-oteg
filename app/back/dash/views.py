from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.



@login_required(login_url='login')
def dash (request):
    username = request.user.username
    return render(request, 'dash/dash.html' , {"username": username})
