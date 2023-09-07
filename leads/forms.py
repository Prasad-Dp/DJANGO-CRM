from django import forms
from . import models
from django.contrib.auth.forms import UserCreationForm,UsernameField
from django.contrib.auth import get_user_model

User=get_user_model()

class LeadForm(forms.ModelForm):
    class Meta:
        model=models.Lead
        fields=(
            'frist_name',
            'last_name',
            'age',
            'organisation',
            'agent',
            'category',
        )

class LeadModelForm(forms.Form):
    frist_name=forms.CharField()
    last_name=forms.CharField()
    age=forms.IntegerField()

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username",)
        field_classes = {'username': UsernameField}

