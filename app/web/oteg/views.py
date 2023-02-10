from django.shortcuts import render

# Create your views here.
def oteg(request):
    return render(request, 'web/paginas/oteg.html')