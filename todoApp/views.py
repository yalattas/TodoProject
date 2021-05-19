from django.shortcuts import render, redirect, get_object_or_404

# To import form from Django
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

# To import Django User model and utilize it
from django.contrib.auth.models import User

# To import Error handling
from django.db import IntegrityError

# To maintain user session and allow him to login
from django.contrib.auth import login, logout, authenticate

# To be used as a form to allow user to submit data into the model/DB
from .forms import TodoForm

# Required to use the model in the view or business logic
from .models import Todo

from django.utils import timezone

# Prevent visitors from accessing certain pages
from django.contrib.auth.decorators import login_required

# Create your views here.
def mainPage(request):
    return render(request, 'pages/index.html')
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
                # You can call you own login method but you need valid credentials
                login(request, user)
                return redirect('current_todos')
            # Require library import
            except IntegrityError:
                return render(request, "pages/sign_up_user.html", {'form': UserCreationForm(), 'errorMessage':'Username taken'})
        else:
            # Password is not matched message with special message shown
            return render(request, "pages/sign_up_user.html", {'form': UserCreationForm(), 'errorMessage':'Password did not match'})

# login_required requires import at the top
@login_required
def log_out(request):
    # Chrome will automatically open many href and maybe log out user accidentally. That's why we look for POST only NOT GET
    if request.method == 'POST':
        logout(request)
        return redirect('mainPage')
    else:
        return redirect('mainPage')

def log_in(request):
    # Require import AuthenticationForm
    if request.method == 'GET':
        return render(request, 'pages/login.html', {'form': AuthenticationForm()})
    else:
        # Require import authenticate to check credentials against DB records
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'pages/login.html', {'form': AuthenticationForm(), 'errorMessage':'Wrong username or password'})
        else:
            login(request, user)
            return redirect('current_todos')

@login_required
# Requires to import a forms model aligned with the chosen fields
def create_todo(request):
    if request.method == 'GET':
        return render(request, 'pages/create_todo.html',{'form':TodoForm()})
    else:
        try:
            # Must be same object as the forms class in order to match, this function will take user inputs and process it
            form = TodoForm(request.POST)
            # Commit will prevent from saving in the DB to do some appliation layer processing
            new_todo_object = form.save(commit=False)
            #To link the object with the user in the DB
            new_todo_object.user = request.user
            new_todo_object.save()
            return redirect('current_todos')
        # Error code "ValueError" taken from the generated error in the web
        # Its meant to prevent user from crossing DB validation or field restrictions
        except ValueError:
            return render(request, 'pages/create_todo.html', {'form': TodoForm(), 'errorMessage':'Bad data entered'})

@login_required
def current_todos(request):
    # Require to import the model at the top, all() mean get all todos regardless of the user
    # todos = Todo.objects.all()
    # to return objects specific to signed in user
    todos = Todo.objects.filter(user=request.user, date_completed__isnull=True)

    return render(request, 'pages/current_todos.html', {'todoObjs':todos})

# todo_pk is coming from the URL file as a variable
@login_required
def view_todo(request, todo_pk):
    #require to import get_object_or_404
    todo_detail = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == 'GET':
        formData = TodoForm(instance=todo_detail)
        return render(request, 'pages/todo_details.html', {'todoID': todo_detail, 'formDetails': formData})
    else:
        try:
            form = TodoForm(request.POST, instance=todo_detail)
            form.save()
            return redirect('current_todos')
        except ValueError:
            return render(request, 'pages/todo_details.html', {'todoID': todo_detail, 'formDetails': form, 'errorMessage':'Bad data entered'})

@login_required
def completed_todo(request):
    completed_todos = Todo.objects.filter(user=request.user, date_completed__isnull=False).order_by('-date_completed')
    return render(request, 'pages/completed_todos.html', {'comp_todos':completed_todos})

@login_required
def complete_todo(request, todo_pk):
    if request.method == 'POST':
        todo_detail = get_object_or_404(Todo, pk=todo_pk, user=request.user)
        # Timezone needs to be imported at the very top of this page
        todo_detail.date_completed = timezone.now()
        todo_detail.save()
        return redirect('current_todos')
    else:
        return redirect('current_todos')

@login_required
def delete_todo(request, todo_pk):
    if request.method == 'POST':
        todo_details = get_object_or_404(Todo, pk=todo_pk, user=request.user)
        todo_details.delete()
        return redirect('current_todos')
    else:
        return redirect('current_todos')