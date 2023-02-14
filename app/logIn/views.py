import re
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages

from .forms import CustomUserCreationForm, ProfileForm, UserForm ,PasswordChangeFormCustom
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
            return redirect('dashboard:publicacion_list')
        else:
            messages.success(req, 'Usuario o Contraseña Incorrectos')
            return redirect('login:login')

    else:
        return render(req, 'back/auth/logIn.html', {})


def logOutUser(req):
    logout(req)
    return redirect('home')


@login_required(login_url='login')
@user_passes_test(lambda u: u.has_perm("auth.view_user"))
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
                return redirect('dashboard:publicacion_list')
    else:
        form = CustomUserCreationForm(req.POST)

    return render(req, 'back/auth/register_user.html', {
        'form': form,
    })


def profile(req):
    bio = Profile.objects.get(user=req.user)
    return render(req, 'back/auth/logIn.html', {})


@login_required(login_url='login')
def users_crud(req):
    users = User.objects.all()

    context = {
        'users': users,
        'request': req

    }

    return render(req, 'back/auth/users_crud.html', {'users': users})


@login_required(login_url='login')
def delete_user(req, user_id):
    User.objects.get(id=user_id).delete()
    return redirect('users_crud')


@login_required(login_url='login')
def edit_user_pwd(req):
    if req.method == 'POST':
        form = PasswordChangeFormCustom(req.user, req.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(req, user)
            return redirect('dashboard:publicacion_list')
    else:
        form = PasswordChangeFormCustom(req.user)
    return render(req, 'back/auth/edit_user_pwd.html', {
        'form': form
    })


@login_required(login_url='login')
def edit_user(req, user_id):
    user = User.objects.get(id=user_id)
    profile = user.profile

    if req.method == 'POST':
        form = ProfileForm(req.POST, req.FILES, instance=profile)
        from_2 = UserForm(req.POST,instance=user)

        if form.is_valid() and from_2.is_valid():
            form.save()
            from_2.save()
            return redirect('users_crud')

    else:
        form = ProfileForm(instance=profile)
        from_2 = UserForm(instance=user)

    return render(req, 'back/auth/edit_user2.html', {'form': form, "form_2": from_2,  'user': user})
