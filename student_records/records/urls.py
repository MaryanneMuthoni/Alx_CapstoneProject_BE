# records/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # example endpoint
    path('', views.index, name='records-index'),
]

