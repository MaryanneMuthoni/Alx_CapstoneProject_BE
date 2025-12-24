from django.shortcuts import render
from django.contrib.auth.models import User
from django.views.generic import CreateView, TemplateView
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm

# Create your views here.

# User Authentication views
# =========================
class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'records/signup.html'

class TemplateView(TemplateView):
    '''Rendering the profile.html template'''
    template_name = 'accounts/profile.html'
