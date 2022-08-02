import django


from django import forms
from .models import Task

class CreateClass(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'desciption', 'complete']


