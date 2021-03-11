from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class SignupForm(UserCreationForm):
    username = forms.CharField(max_length=50, required=True)
    email = forms.EmailField(max_length=256, required=False, help_text='Enter your email (for password recovery purposes only)')

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']