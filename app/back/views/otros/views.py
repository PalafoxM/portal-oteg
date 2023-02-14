from django.shortcuts import render, redirect, get_object_or_404
from back.models import SeccionesCentroDocumental, Categorias
from back.forms import SeccionCentroDocumentalForm
from back.forms import CategoriasForm
from django.urls import reverse_lazy

# Create your views here.


def centro_documental(req):
    secciones = SeccionesCentroDocumental.objects.all()
    context = {
        'secciones': secciones,
    }
    return render(req, 'back/otros/otros/centro_documental.html', context)

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
    return render(request, 'back/otros/otros/add_categoria.html', {'form': form})


def delete_seccion(request, seccion_id):
    seccion = SeccionesCentroDocumental.objects.get(id=seccion_id)

    if request.method == 'POST':
        seccion.delete()
        return redirect('centrodocumental')
    else:
        return render(request, 'back/otros/otros/centro_documental.html', {'seccion': seccion})


def edit_seccion(request, seccion_id):

    seccion = SeccionesCentroDocumental.objects.get(id=seccion_id)

    if request.method == 'POST':
        form = SeccionCentroDocumentalForm(request.POST, instance=seccion)
        if form.is_valid():
            form.save()
            return redirect('centrodocumental')
    else:
        form = SeccionCentroDocumentalForm(instance=seccion)

    return render(request, 'back/otros/otros/edit_seccion.html', {'form': form})


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
    return render(request, 'back/otros/otros/add_categoria.html', {'form': form})


def descargas_list(request):
    data = {
        'title': 'Listado de Banners',
        'descargas': [{'name': 'Listado de Boletín'},{'name': 'Listado de Colaboradores'}],
        'create_url': '#' #reverse_lazy('dashboard:descraga_create')
    }
    return render(request, 'back/descargas/list.html', data)