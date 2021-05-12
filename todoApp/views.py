from django.shortcuts import render, redirect

# To import form from Django
from django.contrib.auth.forms import UserCreationForm

# To import Django User model and utilize it
from django.contrib.auth.models import User

# To import Error handling
from django.db import IntegrityError

# To maintain user session and allow him to login
from django.contrib.auth import login, logout

# Create your views here.
def mainPage(request):
    return redirect('sign_up')
def sign_up(request):
    if request.method == 'GET':
        #To utilize Django Form in view
        return render(request, "pages/sign_up_user.html", {'form':UserCreationForm()})
    else:
        #Validate if 2 password fields are identical
        if request.POST['password1'] == request.POST['password2']:
            try:
                #Create a new user
                user = User.objects.create_user(request.POST['username'], password=request.POST['password2'])
                user.save()
                login(request, user)
                return redirect('current_todos')
            # Require library import
            except IntegrityError:
                return render(request, "pages/sign_up_user.html", {'form': UserCreationForm(), 'errorMessage':'Username taken'})
        else:
            # Password is not matched message with special message shown
            return render(request, "pages/sign_up_user.html", {'form': UserCreationForm(), 'errorMessage':'Password did not match'})

def current_todos(request):
    return render(request, 'pages/current_todos.html')

def log_out(request):
    # Chrome will automatically open many href and maybe log out user accidentally. That's why we look for POST only NOT GET
    if request.method == 'POST':
        logout(request)
        return redirect('mainPage')
    else:
        return redirect('mainPage')