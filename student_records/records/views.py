from django.shortcuts import render
from django.views.generic import CreateView, UpdateView, ListView, DetailView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from .models import Student
from .forms import StudentForm
from django.contrib.auth.decorators import user_passes_test


# Create your views here.

# Functions to check roles defined in UserProfile model
# =====================================================
def is_admin(user):
    '''Checks if user has a profile and is admin, returns True/False'''
    return hasattr(user, 'userprofile') and user.userprofile.role.lower() == 'admin'

def is_student(user):
    '''Checks if user has a profile and is student, returns True/False'''
    return hasattr(user, 'userprofile') and user.userprofile.role.lower() == 'student'

def is_teacher(user):
    '''Checks if user has a profile and is a teacher, returns True/False'''
    return hasattr(user, 'userprofile') and user.userprofile.role.lower() == 'teacher'

def is_parent(user):
    '''Checks if user has a profile and is a parent, returns True/False'''
    return hasattr(user, 'userprofile') and user.userprofile.role.lower() == 'parent'

def is_pending(user):
    '''
    For user who just registered, waiting for approval, returns True/False
    To ensure the right people access the records
    '''
    return hasattr(user, 'userprofile') and user.userprofile.role.lower() == 'pending'


# Views for the different roles once logged in
# ============================================
@user_passes_test(is_admin, login_url='pending')
def admin_view(request):
    '''Renders view for user who is admin'''
    return render(request, 'records/admin_view.html')

@user_passes_test(is_student, login_url='pending')
def student_view(request):
    '''Renders view for user who is student'''
    return render(request, 'records/student_view.html')

@user_passes_test(is_teacher, login_url='pending')
def teacher_view(request):
    '''Renders view for user who is a teacher'''
    return render(request, 'records/teacher_view.html')

@user_passes_test(is_parent, login_url='pending')
def parent_view(request):
    '''Renders view for user who is a parent'''
    return render(request, 'records/parent_view.html')

@login_required
def pending_view(request):
    '''Renders view for users who registered, waiting approval and role assignment'''
    return render(request, 'accounts/pending_view.html')

@login_required
def login_redirect(request):
    '''Redirects after login, 'LOGIN_REDIRECT_URL...' setting in settings.py'''
    user = request.user

    if is_pending(user):
        return redirect('pending')
    elif is_admin(user):
        return redirect('admin_view')
    elif is_teacher(user):
        return redirect('teacher_view')
    elif is_student(user):
        return redirect('student_view')
    elif is_parent(user):
        return redirect('parent_view')
    else:
        return redirect('login')


# Student model views for CRUD operations
# =======================================
class StudentListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    '''
    display all student records, login required for Admin or Teacher
    Student and parents  only views their own/their children's  records
    '''
    model = Student
    template_name = 'records/student_list.html'
    context_object_name = 'students'

    def test_func(self):
        '''
        A test that the current logged-in user must pass 
        to access the view- must be admin/teacher/student/parent
        '''
        user = self.request.user
        return is_admin(user) or is_teacher(user) or is_student(user) or is_parent(user)

    def get_queryset(self):
        '''Restrict students and parents to view of their own/their children's records'''
        user = self.request.user

        # For students
        if is_student(user):
            return Student.objects.filter(user=user)
        # For parents
        elif is_parent(user):
            return Student.objects.filter(parents__parent__user=user)
        # For teacher and admin
        else:
            return Student.objects.all()

class StudentDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    '''
    show details of a specific student
    Student/Parents view only their/their children's records
    Teacher and admins can access any student
    '''
    model = Student
    template_name = 'records/student_detail.html'
    context_object_name = 'student'

    def test_func(self):
        '''
        A test that the current logged-in user must pass 
        to access the view- must be parent/admin/teacher/student
        '''
        user = self.request.user
        return is_admin(user) or is_teacher(user) or is_student(user) or is_parent(user)

    def get_object(self):
        '''
        override get_object method
        '''
        user = self.request.user
        pk = self.kwargs['pk']

        # For students
        if is_student(user):
            return Student.objects.get(pk=pk, user=user)
        # For parents
        elif is_parent(user):
            return Student.objects.get(pk=pk, parents__parent__user=user)
        # For admin and teachers
        return super().get_object()

class StudentCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    '''allow admins to add new students'''
    model = Student
    form_class = StudentForm
    template_name = 'records/student_create.html'
    success_url = reverse_lazy('students')

    def test_func(self):
        '''A test that the current logged-in user must pass to access the view- must be admin'''
        return is_admin(self.request.user)

class StudentUpdateView(LoginRequiredMixin, UserPassesTestMixin,UpdateView):
    '''enable admin to edit student records'''
    model = Student
    form_class = StudentForm
    template_name = 'records/student_update.html'
    success_url = reverse_lazy('students')
    context_object_name = 'student'

    def test_func(self):
        '''A test that the current logged-in user must pass to access the view- must be admin'''
        return is_admin(self.request.user)

class StudentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    '''let admin delete student records'''
    model = Student
    template_name = 'records/student_delete.html'
    success_url = reverse_lazy('students')

    def test_func(self):
        '''A test that the current logged-in user must pass to access the view- must be admin'''
        return is_admin(self.request.user)
