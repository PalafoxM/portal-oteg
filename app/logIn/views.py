import re
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from .forms import CustomUserCreationForm, CustomUserUpdateForm, ProfileForm, UserForm ,PasswordChangeFormCustom
from .models import User, Profile
from django.views.generic import ListView, CreateView, UpdateView
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse_lazy


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
            return redirect('dashboard:fuente_informacion')
        else:
            messages.success(req, 'Usuario o Contraseña Incorrectos')
            return redirect('login_user')
    else:
        return render(req, 'back/auth/logIn.html', {})


def logOutUser(req):
    logout(req)
    return redirect('inicio')


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
                return redirect('dashboard:fuente_informacion')
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
    return redirect('usuarios-list')


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

    return render(req, 'back/auth/edit_user2.html', {'form': form, "form_2": from_2, 'user': user})


class UserListView( ListView):
    model = User
    template_name = 'back/auth/users_crud.html'

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search':
                data = []
                for i in User.objects.all():
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Usuarios'
        context['create_url'] = reverse_lazy('usuarios-perfil-create')
        context['list_url'] = reverse_lazy('usuarios-list')
        context['entity'] = 'Usuarios'
        return context
    

class UserAndProfileCreateView(CreateView):
    model = User
    form_class = CustomUserCreationForm
    template_name = 'back/components/create_update.html'
    success_url = reverse_lazy('usuarios-list') 

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        profile_form = ProfileForm(request.POST, request.FILES)
        print("paso 1 post")
        if form.is_valid() and profile_form.is_valid():
            print("paso 2 post")
            email = form.cleaned_data.get('email')
            if User.objects.filter(email=email).exists():
                form.add_error('email', 'Ya existe un usuario con este correo electrónico.')
                data = {
                    'success': False,
                    'message': 'Hubo un error al crear el usuario y/o perfil.',
                    'errors': form.errors
                }
                return JsonResponse(data)
            user = form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            # profile.save()
            data = {
                'success': True,
                'message': 'Usuario y perfil creados exitosamente.',
                'url': self.success_url
            }
            return JsonResponse(data)
        else:
            print("paso 3 post")
            errors = {}
            # Agregar los errores del formulario de usuario
            for field, error in form.errors.items():
                errors[field] = error.as_text()
            # Agregar los errores del formulario de perfil
            for field, error in profile_form.errors.items():
                errors[field] = error.as_text()
            data = {
                'success': False,
                'message': 'Hubo un error al crear el usuario y/o perfil.',
                'errors': errors 
            }
            return JsonResponse(data)

    def form_invalid(self, form):
        print("paso 2")
        response = super().form_invalid(form)
        # Verificar si ya existe un usuario con el mismo correo electrónico
        email = form.cleaned_data.get('email')
        if email and User.objects.filter(email=email).exists():
            print("paso 1 form_invalid")
            form.add_error('email', 'Ya existe un usuario con este correo electrónico.')
        # Verificar si ya existe un usuario con el mismo nombre de usuario
        username = form.cleaned_data.get('username')
        if username and User.objects.filter(username=username).exists():
            print("paso 2 form_invalid")
            form.add_error('username', 'Ya existe un usuario con este nombre de usuario.')
        # Devolver la respuesta con los errores correspondientes
        errors = {}
        for field, error in form.errors.items():
            errors[field] = error.as_text()
        data = {
            'success': False,
            'message': 'Hubo un error al crear el usuario y/o perfil.',
            'errors': errors 
        }
        return JsonResponse(data)

    def form_valid(self, form):
        print("paso 1 form_valid")
        response = super().form_valid(form)
        profile_form = ProfileForm(self.request.POST, self.request.FILES)
        if profile_form.is_valid():
            print("paso 2 form_valid")
            profile = profile_form.save(commit=False)
            profile.user = self.object
            profile.save()
        data = {
            'success': True,
            'message': 'Usuario y perfil creados exitosamente.',
            'url': self.success_url
        }
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['profile_form'] = ProfileForm(self.request.POST, self.request.FILES)
        else:
            context['profile_form'] = ProfileForm()

        context['title'] = 'Crear Usuario'
        context['entity'] = 'Usuarios'
        context['list_url'] = reverse_lazy('usuarios-list')
        return context


class UserAndProfileUpdateView(UpdateView):
    model = User
    form_class = CustomUserUpdateForm
    template_name = 'back/components/create_update.html'
    success_url = reverse_lazy('usuarios-list')

    def get_object(self, queryset=None):
        return self.model.objects.get(pk=self.kwargs['pk'])

    def form_valid(self, form):
        response = super().form_valid(form)
        # user_form = form.save(commit=False)
        profile = self.object.profile  # Obtener la instancia del perfil del usuario
        profile_form = ProfileForm(self.request.POST, self.request.FILES, instance=profile)
        
        # Verificar si ya existe un usuario con el mismo correo electrónico
        email = form.cleaned_data.get('email')
        if email:
            if User.objects.filter(email=email).exclude(pk=self.object.pk).exists():
                form.add_error('email', 'Ya existe un usuario con este correo electrónico.')
                return self.form_invalid(form)

        # Verificar si ya existe un usuario con el mismo nombre de usuario
        username = form.cleaned_data.get('username')
        if username:
            if User.objects.filter(username=username).exclude(pk=self.object.pk).exists():
                form.add_error('username', 'Ya existe un usuario con este nombre de usuario.')
                return self.form_invalid(form)
            
        if form.is_valid() and profile_form.is_valid():
            profile = profile_form.save(commit=False)
            profile.user = self.object
            if Profile.objects.filter(user=self.object).exists():
                profile.save()  # Actualiza el objeto del perfil con los nuevos datos
            else:
                profile_form.save()  # Crea un nuevo objeto del perfil y guarda sus datos
        form.save()
        data = {
            'success': True,
            'message': 'Usuario y perfil actualizados exitosamente.',
            'url': self.success_url
        }
        
        if is_ajax(self.request):
            return JsonResponse(data)
        else:
            return response

    def form_invalid(self, form):
        print("paso 1")
        response = super().form_invalid(form)

        # Define profile_form here
        profile = self.object.profile
        profile_form = ProfileForm(self.request.POST, self.request.FILES, instance=profile)
        
                
        if form.errors or profile_form.errors:
            print("paso 4")
            data = {
                'success': False,
                'message': 'Hubo un error al actualizar el usuario y/o perfil.',
                'errors':  form.errors
            }
        else:
            
            print("profile_form: ", profile_form.errors)
            print("form: ", form.errors)

            print("paso 5")
            data = {
            'success': True,
            'message': 'Usuario actualizado exitosamente.',
            'url': self.success_url
            }
            
        if is_ajax(self.request):
            return JsonResponse(data)
        else:
            return response
            
        

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = Profile.objects.get(user=self.object)
        context['title'] = 'Editar Usuario'
        context['entity'] = 'Usuarios'
        context['list_url'] = reverse_lazy('usuarios-list')
        context['profile_form'] = ProfileForm(instance=profile)
        return context
    

def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'