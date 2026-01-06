from django.shortcuts import render
from django.contrib.auth.models import User
from django.views.generic import CreateView, TemplateView
from django.urls import reverse_lazy
from .forms import UserCreationCustomForm

# Create your views here.

# User Authentication views
# =========================
class SignUpView(CreateView):
    form_class = UserCreationCustomForm
    success_url = reverse_lazy('login')
    template_name = 'records/signup.html'

class TemplateView(TemplateView):
    '''Rendering the profile.html template'''
    template_name = 'accounts/profile.html'
