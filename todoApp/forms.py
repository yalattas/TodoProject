from django.forms import ModelForm
from .models import Todo

# Require to import the Form model created by Django framework
class TodoForm(ModelForm):
    class Meta:
        # Require to import the model first
        model = Todo
        fields = [
            'title',
            'memo',
            'important',
        ]