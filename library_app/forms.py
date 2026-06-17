from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm

from .models import User


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