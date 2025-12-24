# records/urls.py
from django.urls import path
from .views import admin_view, student_view, teacher_view, parent_view, pending_view, login_redirect, StudentListView, StudentDetailView, StudentCreateView, StudentUpdateView, StudentDeleteView
# from . import views

urlpatterns = [
    path('admin_view/', admin_view, name='admin_view'),
    path('student_view/', student_view, name='student_view'),
    path('teacher_view/', teacher_view, name='teacher_view'),
    path('parent_view/', parent_view, name='parent_view'),
    path('pending/', pending_view, name='pending_view'),
    path('login_redirect/', login_redirect, name='login_redirect'),
    path('students/', StudentListView.as_view(), name='student_list'),
    path('student/<int:pk>/', StudentDetailView.as_view(), name='student_detail'),
    path('student/new/', StudentCreateView.as_view(), name='student_create'),
    path('student/<int:pk>/update/', StudentUpdateView.as_view(), name='student_update'),
    path('student/<int:pk>/delete/', StudentDeleteView.as_view(), name='student_delete'),
]

