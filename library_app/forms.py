from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.forms import ModelForm
from .models import *


class RegisterForm(UserCreationForm):

    class Meta:
        model = User

        fields = [
            'username',
            'email',
            'role',
            'password1',
            'password2',
        ]


class LoginForm(AuthenticationForm):
    username = forms.CharField()
    password = forms.CharField(
        widget=forms.PasswordInput
    )
    
    
class BookForm(ModelForm):

    class Meta:
        model = Book

        fields = [
            'title',
            'isbn',
            'total_copies',
        ]