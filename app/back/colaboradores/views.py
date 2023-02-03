from django.shortcuts import render

# Create your views here.
def publicaciones_list(request):
    data = {

    }
    return render(request, 'publicaciones/list.html', data)