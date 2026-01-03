from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class UserCreationCustomForm(UserCreationForm):
    '''
    Custom form for user registration with default fields:
    username, email, password and additional fields: profile_picture 
    and phone_number
    '''
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'phone_number', 'profile_photo')
