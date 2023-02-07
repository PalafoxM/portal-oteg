from django.shortcuts import render, redirect, get_object_or_404
from .models import SeccionesCentroDocumental, Categorias
from .forms import SeccionCentroDocumentalForm
from .forms import CategoriasForm

# Create your views here.


def centro_documental(req):
    secciones = SeccionesCentroDocumental.objects.all()
    context = {
        'secciones': secciones,
    }
    return render(req, 'otros/centro_documental.html', context)

# def add_categoria(req):
#     secciones = SeccionesCentroDocumental.objects.all()
#     context = {
#         'secciones': secciones,
#     }
#     return render(req, 'otros/add_categoria.html', context)


def add_seccion_centro_documental(request):
    if request.method == 'POST':
        form = SeccionCentroDocumentalForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('centrodocumental')
    else:
        form = SeccionCentroDocumentalForm()
    return render(request, 'otros/add_categoria.html', {'form': form})


def delete_seccion(request, seccion_id):
    seccion = SeccionesCentroDocumental.objects.get(id=seccion_id)

    if request.method == 'POST':
        seccion.delete()
        return redirect('centrodocumental')
    else:
        return render(request, 'otros/centro_documental.html', {'seccion': seccion})


def edit_seccion(request, seccion_id):

    seccion = SeccionesCentroDocumental.objects.get(id=seccion_id)

    if request.method == 'POST':
        form = SeccionCentroDocumentalForm(request.POST, instance=seccion)
        if form.is_valid():
            form.save()
            return redirect('centrodocumental')
    else:
        form = SeccionCentroDocumentalForm(instance=seccion)

    return render(request, 'otros/edit_seccion.html', {'form': form})


def add_categoria(request, seccion_id):

    seccion = SeccionesCentroDocumental.objects.get(id=seccion_id)
    if request.method == 'POST':
        form = CategoriasForm(request.POST)
        if form.is_valid():
            categoria = form.save(commit=False)
            categoria.seccion = seccion
            categoria.save()
            return redirect('centrodocumental')
    else:
        form = CategoriasForm()
    return render(request, 'otros/add_categoria.html', {'form': form})
