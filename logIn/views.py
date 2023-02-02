import re
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages

# Create your views here.


def logInUser(req):

    # def validate(string):
    #     pattern = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]+$')
    #     match = pattern.search(string)
    #     return bool(match)

    if req.method == 'POST':

        username = req.POST.get('usuario')
        password = req.POST.get('pwd')

        print(username,password)

        user = authenticate(req,username=username,password=password)

        if user is not None:
            # if not validate(password):
            #     messages.success(req,'Contraseña no cumple con los requisitos')
            #     return redirect('login')
            # else:

                login(req,user)
                return redirect('home')
        else:
            messages.success(req,'Usuario o Contraseña Incorrectos')
            return redirect('login')
          
    else:
        return render(req,'auth/logIn.html',{})


def logOutUser(req):
    logout(req)
    return redirect('home')