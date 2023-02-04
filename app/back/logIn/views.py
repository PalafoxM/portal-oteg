import re
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from .models import Profile
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm
from .forms import ImageUploadForm
from .models import User, Profile

# Create your views here.


def logInUser(req):

    if req.method == 'POST':

        username = req.POST.get('usuario')
        password = req.POST.get('pwd')

        print(username, password)

        user = authenticate(req, username=username, password=password)

        if user is not None:
            # if not validate(password):
            #     messages.success(req,'Contraseña no cumple con los requisitos')
            #     return redirect('login')
            # else:

            login(req, user)
            return redirect('dash')
        else:
            messages.success(req, 'Usuario o Contraseña Incorrectos')
            return redirect('login')

    else:
        return render(req, 'auth/logIn.html', {})


def logOutUser(req):
    logout(req)
    return redirect('home')


@login_required(login_url='login')
def register_user(req):

    def validate(string):
        pattern = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]+$')
        match = pattern.search(string)
        return bool(match)

    if req.method == 'POST':

        form = CustomUserCreationForm(req.POST, req.FILES)

        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')

            if not validate(password):
                messages.success(
                    req, 'Contraseña no cumple con los requisitos , Utilizar al menos un carácter alfanumérico, una letra mayúscula, minúscula ')
            else:
                form.save()
                user = authenticate(req, username=username, password=password)
                login(req, user)
                messages.success(req, 'Usuario creado exitosamente')
                return redirect('dash')
    else:
        form = CustomUserCreationForm(req.POST)

    return render(req, 'auth/register_user.html', {
        'form': form,
    })


def profile(req):
    bio = Profile.objects.get(user=req.user)
    return render(req, 'auth/logIn.html', {})


@login_required(login_url='login')
def users_crud(req):
    users = User.objects.all()

    return render(req, 'auth/users_crud.html', {'users': users})


@login_required(login_url='login')
def delete_user(req, user_id):
    User.objects.get(id=user_id).delete()
    return redirect('users_crud')


@login_required(login_url='login')
def edit_user(req, user_id):

    user = User.objects.get(id=user_id)
    profile = user.profile

    if req.method == 'POST':

        form = ImageUploadForm(req.POST, req.FILES)

        if form.is_valid():
            photo = form.cleaned_data['image']
            # save the photo to the model
            new_photo = Profile(photo=photo)
            new_photo.save()

        user.username = req.POST['username']
        user.first_name = req.POST['first_name']
        user.last_name = req.POST['last_name']
        profile.apellido_materno = req.POST['apellido_materno']
        profile.apellido_paterno = req.POST['last_name']
        profile.fecha_cumple = req.POST['fecha_cumple']
        user.email = req.POST['email']
        profile.tel = req.POST['tel']
        profile.facebook = req.POST['facebook']
        profile.twitter = req.POST['twitter']
        profile.ciudad = req.POST['ciudad']
        profile.estado = req.POST['estado']
        profile.empresa_institucion = req.POST['empresa_institucion']
        profile.cargo = req.POST['cargo']
        profile.licenciatura = req.POST['licenciatura']
        profile.universidad_licenciatura = req.POST['universidad_licenciatura']
        profile.maestria = req.POST['maestria']
        profile.universidad_maestria = req.POST['universidad_maestria']
        profile.doctorado = req.POST['doctorado']
        profile.universidad_doctorado = req.POST['universidad_doctorado']
        profile.experiencia = req.POST['experiencia']
        profile.boletin = req.POST['boletin']

        user.save()
        profile.save()
        return redirect('users_crud')

    else:
        form = ImageUploadForm()

    return render(req, 'auth/edit_user.html', {'user': user, 'profile': profile, 'form': form})
