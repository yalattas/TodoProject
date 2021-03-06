"""TodoProj URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from todoApp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.mainPage, name='mainPage'),

    # Auth
    path('signup/', views.sign_up, name='sign_up'),
    path('logout/', views.log_out, name='log_out'),
    path('login/', views.log_in, name='log_in'),

    # Todos
    path('current/', views.current_todos, name='current_todos'),
    path('create/', views.create_todo, name='create_todo'),
    path('completed/', views.completed_todo, name='completed_todo'),
    path('todo/<int:todo_pk>', views.view_todo, name='view_todo'),

    # Post actions without a views
    path('todo/<int:todo_pk>/complete', views.complete_todo, name='complete_todo'),
    path('todo/<int:todo_pk>/delete', views.delete_todo, name='delete_todo'),
]
