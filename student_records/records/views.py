from django.shortcuts import render, redirect
from django.views.generic import CreateView, UpdateView, ListView, DetailView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from .models import Student, Parent, Grade, Teacher, Performance, Attendance, Invoice, Payment, Enrollment, Subject
from .forms import StudentForm, ParentForm, GradeForm, TeacherForm, PerformanceForm, AttendanceForm, InvoiceForm, PaymentForm, EnrollmentForm, SubjectForm
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


# Parent model views for CRUD operations
# =======================================
class ParentListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    '''
    display all parent records
    Student and parents only view their own/their parents'/guardians' records
    '''
    model = Parent
    template_name = 'records/parent_list.html'
    context_object_name = 'parents'

    def test_func(self):
        '''
        A test that the current logged-in user must pass 
        to access the view- must be admin/teacher/student/parent
        '''
        user = self.request.user
        return is_admin(user) or is_teacher(user) or is_student(user) or is_parent(user)

    def get_queryset(self):
        '''Restrict parents/students to view of their own/their parent's records'''
        user = self.request.user

        # For students
        if is_student(user):
            return Parent.objects.filter(user=user)
        # For parents
        elif is_parent(user):
            return Parent.objects.filter(students__student=user.student_profile)
        # For teacher and admin
        else:
            return Parent.objects.all()

class ParentDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    '''
    show details of a specific parent
    Parents/Students view only their/their parents'/guardians' records
    Teacher and admins can access any parent
    '''
    model = Parent
    template_name = 'records/parent_detail.html'
    context_object_name = 'parent'

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
            return Parent.objects.get(pk=pk, user=user)
        # For parents
        elif is_parent(user):
            return Parent.objects.get(pk=pk, students__student=user.student_profile)
        # For admin and teachers
        return super().get_object()

class ParentCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    '''allow admins to add new parents/guardians'''
    model = Parent
    form_class = ParentForm
    template_name = 'records/parent_create.html'
    success_url = reverse_lazy('parents')

    def test_func(self):
        '''A test that the current logged-in user must pass to access the view- must be admin'''
        return is_admin(self.request.user)

class ParentUpdateView(LoginRequiredMixin, UserPassesTestMixin,UpdateView):
    '''enable admin to edit student records'''
    model = Parent
    form_class = ParentForm
    template_name = 'records/parent_update.html'
    success_url = reverse_lazy('parents')
    context_object_name = 'parent'

    def test_func(self):
        '''A test that the current logged-in user must pass to access the view- must be admin'''
        return is_admin(self.request.user)

class ParentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    '''let admin delete parent records'''
    model = Parent
    template_name = 'records/parent_delete.html'
    success_url = reverse_lazy('parents')

    def test_func(self):
        '''A test that the current logged-in user must pass to access the view- must be admin'''
        return is_admin(self.request.user)

# Grade model views for CRUD operations
# =======================================
class GradeListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    '''
    display all grade records
    Student and parents only view their own/their parents'/guardians' record
    '''
    model = Grade
    template_name = 'records/grade_list.html'
    context_object_name = 'grades'

    def test_func(self):
        '''
        A test that the current logged-in user must pass 
        to access the view- must be admin/teacher/student/parent
        '''
        user = self.request.user
        return is_admin(user) or is_teacher(user) or is_student(user) or is_parent(user)

    def get_queryset(self):
        '''Restrict parents/students to view of their own/their parent's records'''
        user = self.request.user

        # For students
        if is_student(user):
            return Grade.objects.filter(students=user.student_profile)
        # For parents
        elif is_parent(user):
            return Grade.objects.filter(students__in=user.parent_profile.students.all())
        # For teacher and admin
        else:
            return Grade.objects.all()

class GradeDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    '''
    show details of a specific grade
    Students/Parents view only their own children's records
    Teacher and admins can access any grade
    '''
    model = Grade
    template_name = 'records/grade_detail.html'
    context_object_name = 'grade'

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
            return Grade.objects.get(pk=pk, students=user.student_profile)
        # For parents
        elif is_parent(user):
            return Grade.objects.get(pk=pk, students__in=user.parent_profile.students.all())
        # For admin and teachers
        return super().get_object()

class GradeCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    '''allow admins to add new grade records'''
    model = Grade
    form_class = GradeForm
    template_name = 'records/grade_create.html'
    success_url = reverse_lazy('grades')

    def test_func(self):
        '''A test that the current logged-in user must pass to access the view- must be admin'''
        return is_admin(self.request.user)

class GradeUpdateView(LoginRequiredMixin, UserPassesTestMixin,UpdateView):
    '''enable admin to edit grade records'''
    model = Grade
    form_class = GradeForm
    template_name = 'records/grade_update.html'
    success_url = reverse_lazy('grades')
    context_object_name = 'grade'

    def test_func(self):
        '''A test that the current logged-in user must pass to access the view- must be admin'''
        return is_admin(self.request.user)

class GradeDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    '''let admin delete grade records'''
    model = Grade
    template_name = 'records/grade_delete.html'
    success_url = reverse_lazy('grades')

    def test_func(self):
        '''A test that the current logged-in user must pass to access the view- must be admin'''
        return is_admin(self.request.user)


# Teacher model views for CRUD operations
# =======================================
class TeacherListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    '''
    display all teacher records for all roles(Admin/Teacher/Student/Parent)
    '''
    model = Teacher
    template_name = 'records/teacher_list.html'
    context_object_name = 'teachers'

    def test_func(self):
        '''
        A test that the current logged-in user must pass 
        to access the view- must be admin/teacher/student/parent
        '''
        user = self.request.user
        return is_admin(user) or is_teacher(user) or is_student(user) or is_parent(user)

class TeacherDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    '''
    show details of a specific teacher to all roles
    '''
    model = Teacher
    template_name = 'records/teacher_detail.html'
    context_object_name = 'teacher'

    def test_func(self):
        '''
        A test that the current logged-in user must pass 
        to access the view- must be parent/admin/teacher/student
        '''
        user = self.request.user
        return is_admin(user) or is_teacher(user) or is_student(user) or is_parent(user)

class TeacherCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    '''allow admins to add new teacher records'''
    model = Teacher
    form_class = TeacherForm
    template_name = 'records/teacher_create.html'
    success_url = reverse_lazy('teachers')

    def test_func(self):
        '''A test that the current logged-in user must pass to access the view- must be admin'''
        return is_admin(self.request.user)

class TeacherUpdateView(LoginRequiredMixin, UserPassesTestMixin,UpdateView):
    '''enable admin to edit grade records'''
    model = Teacher
    form_class = TeacherForm
    template_name = 'records/teacher_update.html'
    success_url = reverse_lazy('teachers')
    context_object_name = 'teacher'

    def test_func(self):
        '''A test that the current logged-in user must pass to access the view- must be admin'''
        return is_admin(self.request.user)

class TeacherDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    '''let admin delete teacher records'''
    model = Teacher
    template_name = 'records/teacher_delete.html'
    success_url = reverse_lazy('teachers')

    def test_func(self):
        '''A test that the current logged-in user must pass to access the view- must be admin'''
        return is_admin(self.request.user)


# Subject model views for CRUD operations
# =======================================
class SubjectListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    '''
    display all subject records for all roles(Admin/Teacher/Student/Parent)
    '''
    model = Subject
    template_name = 'records/subject_list.html'
    context_object_name = 'subjects'

    def test_func(self):
        '''
        A test that the current logged-in user must pass 
        to access the view- must be admin/teacher/student/parent
        '''
        user = self.request.user
        return is_admin(user) or is_teacher(user) or is_student(user) or is_parent(user)

class SubjectDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    '''
    show details of a specific subject to all roles
    '''
    model = Subject
    template_name = 'records/subject_detail.html'
    context_object_name = 'subject'

    def test_func(self):
        '''
        A test that the current logged-in user must pass 
        to access the view- must be parent/admin/teacher/student
        '''
        user = self.request.user
        return is_admin(user) or is_teacher(user) or is_student(user) or is_parent(user)

class SubjectCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    '''allow admins to add new teacher records'''
    model = Subject
    form_class = SubjectForm
    template_name = 'records/subject_create.html'
    success_url = reverse_lazy('subjects')

    def test_func(self):
        '''A test that the current logged-in user must pass to access the view- must be admin'''
        return is_admin(self.request.user)

class SubjectUpdateView(LoginRequiredMixin, UserPassesTestMixin,UpdateView):
    '''enable admin to edit subject records'''
    model = Subject
    form_class = SubjectForm
    template_name = 'records/subject_update.html'
    success_url = reverse_lazy('subjects')
    context_object_name = 'subject'

    def test_func(self):
        '''A test that the current logged-in user must pass to access the view- must be admin'''
        return is_admin(self.request.user)

class SubjectDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    '''let admin delete subject records'''
    model = Subject
    template_name = 'records/subject_delete.html'
    success_url = reverse_lazy('subjects')

    def test_func(self):
        '''A test that the current logged-in user must pass to access the view- must be admin'''
        return is_admin(self.request.user)


# Performance model views for CRUD operations
# =======================================
class PerformanceListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    '''
    display all performance records for Admin/Teacher
    Student/Parent can only view their own/own children's records
    '''
    model = Performance
    template_name = 'records/performance_list.html'
    context_object_name = 'performances'

    def test_func(self):
        '''
        A test that the current logged-in user must pass 
        to access the view- must be admin/teacher/student/parent
        '''
        user = self.request.user
        return is_admin(user) or is_teacher(user) or is_student(user) or is_parent(user)

    def get_queryset(self):
        '''
        Restrict students and parents to view of their own/their children's performance records
        '''
        user = self.request.user

        # For students
        if is_student(user):
            return Performance.objects.filter(student__user=user)
        # For parents
        elif is_parent(user):
            return Performance.objects.filter(student__parents__parent__user=user)
        # For teacher and admin
        else:
            return Performance.objects.all()

class PerformanceDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    '''
    show details of a specific performance
    Admin/Teacher can view all performances
    Students/Parents can see their own/their children's performance
    '''
    model = Performance
    template_name = 'records/performance_detail.html'
    context_object_name = 'performance'

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
            return Performance.objects.get(pk=pk, student__user=user)
        # For parents
        elif is_parent(user):
            return Performance.objects.get(pk=pk, student__parents__parent__user=user)
        # For admin and teachers
        return super().get_object()

class PerformanceCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    '''allow admins to add new teacher records'''
    model = Performance
    form_class = PerformanceForm
    template_name = 'records/performance_create.html'
    success_url = reverse_lazy('performances')

    def test_func(self):
        '''A test that the current logged-in user must pass to access the view- must be admin'''
        return is_admin(self.request.user)

class PerformanceUpdateView(LoginRequiredMixin, UserPassesTestMixin,UpdateView):
    '''enable admin to edit performance records'''
    model = Performance
    form_class = PerformanceForm
    template_name = 'records/performance_update.html'
    success_url = reverse_lazy('performances')
    context_object_name = 'performance'

    def test_func(self):
        '''A test that the current logged-in user must pass to access the view- must be admin'''
        return is_admin(self.request.user)

class PerformanceDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    '''let admin delete performance records'''
    model = Performance
    template_name = 'records/performance_delete.html'
    success_url = reverse_lazy('performances')

    def test_func(self):
        '''A test that the current logged-in user must pass to access the view- must be admin'''
        return is_admin(self.request.user)


# Attendance model views for CRUD operations
# =======================================
class AttendanceListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    '''
    display all attendance records for Admin/Teacher
    Student/Parent can only view their own/own children's records
    '''
    model = Attendance
    template_name = 'records/attendance_list.html'
    context_object_name = 'attendances'

    def test_func(self):
        '''
        A test that the current logged-in user must pass 
        to access the view- must be admin/teacher/student/parent
        '''
        user = self.request.user
        return is_admin(user) or is_teacher(user) or is_student(user) or is_parent(user)

    def get_queryset(self):
        '''
        Restrict students and parents to view of their own/their children's attendance records
        '''
        user = self.request.user

        # For students
        if is_student(user):
            return Attendance.objects.filter(student__user=user)
        # For parents
        elif is_parent(user):
            return Attendance.objects.filter(student__parents__parent__user=user)
        # For teacher and admin
        else:
            return Attendance.objects.all()

class AttendanceDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    '''
    show details of a specific attendance for a student
    Admin/Teacher can view all attendances
    Students/Parents can see their own/their children's attendance
    '''
    model = Attendance
    template_name = 'records/attendance_detail.html'
    context_object_name = 'attendance'

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
            return Attendance.objects.get(pk=pk, student__user=user)
        # For parents
        elif is_parent(user):
            return Attendance.objects.get(pk=pk, student__parents__parent__user=user)
        # For admin and teachers
        return super().get_object()

class AttendanceCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    '''allow admins to add new attendance records'''
    model = Attendance
    form_class = AttendanceForm
    template_name = 'records/attendance_create.html'
    success_url = reverse_lazy('attendances')

    def test_func(self):
        '''A test that the current logged-in user must pass to access the view- must be admin'''
        return is_admin(self.request.user)

class AttendanceUpdateView(LoginRequiredMixin, UserPassesTestMixin,UpdateView):
    '''enable admin to edit performance records'''
    model = Attendance
    form_class = AttendanceForm
    template_name = 'records/attendance_update.html'
    success_url = reverse_lazy('attendances')
    context_object_name = 'attendance'

    def test_func(self):
        '''A test that the current logged-in user must pass to access the view- must be admin'''
        return is_admin(self.request.user)

class AttendanceDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    '''let admin delete attendance records'''
    model = Attendance
    template_name = 'records/attendance_delete.html'
    success_url = reverse_lazy('attendances')

    def test_func(self):
        '''A test that the current logged-in user must pass to access the view- must be admin'''
        return is_admin(self.request.user)


# Invoice model views for CRUD operations
# =======================================
class InvoiceListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    '''
    display all invoice records for Admin
    Student/Parent can only view their own/own children's invoice records
    Teachers can view none of the invoice records
    '''
    model = Invoice
    template_name = 'records/invoice_list.html'
    context_object_name = 'invoices'

    def test_func(self):
        '''
        A test that the current logged-in user must pass 
        to access the view- must be admin/teacher/student/parent
        '''
        user = self.request.user
        return is_admin(user) or is_student(user) or is_parent(user)

    def get_queryset(self):
        '''
        Restrict students and parents to view of their own/their children's invoice records
        '''
        user = self.request.user

        # For students
        if is_student(user):
            return Invoice.objects.filter(student__user=user)
        # For parents
        elif is_parent(user):
            return Invoice.objects.filter(student__parents__parent__user=user)
        # For admin
        else:
            return Invoice.objects.all()

class InvoiceDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    '''
    show details of a specific invoice
    Admin can view all invoices
    Students/Parents can see their own/their children's invoices
    Teachers can view none of the invoice records
    '''
    model = Invoice
    template_name = 'records/invoice_detail.html'
    context_object_name = 'invoices'

    def test_func(self):
        '''
        A test that the current logged-in user must pass 
        to access the view- must be parent/admin/teacher/student
        '''
        user = self.request.user
        return is_admin(user) or is_student(user) or is_parent(user)

    def get_object(self):
        '''
        override get_object method
        '''
        user = self.request.user
        pk = self.kwargs['pk']

        # For students
        if is_student(user):
            return Invoice.objects.get(pk=pk, student__user=user)
        # For parents
        elif is_parent(user):
            return Invoice.objects.get(pk=pk, student__parents__parent__user=user)
        # For teachers
        return super().get_object()

class InvoiceCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    '''allow admins to add new invoice records'''
    model = Invoice
    form_class = InvoiceForm
    template_name = 'records/invoice_create.html'
    success_url = reverse_lazy('invoices')

    def test_func(self):
        '''A test that the current logged-in user must pass to access the view- must be admin'''
        return is_admin(self.request.user)

class InvoiceUpdateView(LoginRequiredMixin, UserPassesTestMixin,UpdateView):
    '''enable admin to edit invoive records'''
    model = Invoice
    form_class = InvoiceForm
    template_name = 'records/invoice_update.html'
    success_url = reverse_lazy('invoices')
    context_object_name = 'invoice'

    def test_func(self):
        '''A test that the current logged-in user must pass to access the view- must be admin'''
        return is_admin(self.request.user)

class InvoiceDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    '''let admin delete invoice records'''
    model = Invoice
    template_name = 'records/invoice_delete.html'
    success_url = reverse_lazy('invoices')

    def test_func(self):
        '''A test that the current logged-in user must pass to access the view- must be admin'''
        return is_admin(self.request.user)


# Payment model views for CRUD operations
# =======================================
class PaymentListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    '''
    display all payment records for Admin
    Student/Parent can only view their own/own children's payment records
    Teachers can view none of the payment records
    '''
    model = Payment
    template_name = 'records/payment_list.html'
    context_object_name = 'payments'

    def test_func(self):
        '''
        A test that the current logged-in user must pass 
        to access the view- must be admin/teacher/student/parent
        '''
        user = self.request.user
        return is_admin(user) or is_student(user) or is_parent(user)

    def get_queryset(self):
        '''
        Restrict students and parents to view of their own/their children's payment records
        '''
        user = self.request.user

        # For students
        if is_student(user):
            return Payment.objects.filter(invoice__student__user=user)
        # For parents
        elif is_parent(user):
            return Payment.objects.filter(invoice__student__parents__parent__user=user)
        # For admin
        else:
            return Payment.objects.all()

class PaymentDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    '''
    show details of a specific payment
    Admin can view all payments
    Students/Parents can see their own/their children's payments
    Teachers can view none of the payment records
    '''
    model = Payment
    template_name = 'records/payment_detail.html'
    context_object_name = 'payment'

    def test_func(self):
        '''
        A test that the current logged-in user must pass 
        to access the view- must be parent/admin/teacher/student
        '''
        user = self.request.user
        return is_admin(user) or is_student(user) or is_parent(user)

    def get_object(self):
        '''
        override get_object method
        '''
        user = self.request.user
        pk = self.kwargs['pk']

        # For students
        if is_student(user):
            return Payment.objects.get(pk=pk, invoice__student__user=user)
        # For parents
        elif is_parent(user):
            return Payment.objects.get(pk=pk, invoice__student__parents__parent__user=user)
        # For admin
        return super().get_object()

class PaymentCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    '''allow admins to add new payment records'''
    model = Payment
    form_class = PaymentForm
    template_name = 'records/payment_create.html'
    success_url = reverse_lazy('payments')

    def test_func(self):
        '''A test that the current logged-in user must pass to access the view- must be admin'''
        return is_admin(self.request.user)

class PaymentUpdateView(LoginRequiredMixin, UserPassesTestMixin,UpdateView):
    '''enable admin to edit payment records'''
    model = Payment
    form_class = PaymentForm
    template_name = 'records/payments_update.html'
    success_url = reverse_lazy('payments')
    context_object_name = 'payment'

    def test_func(self):
        '''A test that the current logged-in user must pass to access the view- must be admin'''
        return is_admin(self.request.user)

class PaymentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    '''let admin delete payment records'''
    model = Payment
    template_name = 'records/payment_delete.html'
    success_url = reverse_lazy('payments')

    def test_func(self):
        '''A test that the current logged-in user must pass to access the view- must be admin'''
        return is_admin(self.request.user)


# Enrollment model views for CRUD operations
# =======================================
class EnrollmentListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    '''
    display all enrollment records for Admin/Teacher
    Student/Parent can only view their own/own children's enrollment records
    '''
    model = Enrollment
    template_name = 'records/enrollment_list.html'
    context_object_name = 'enrollments'

    def test_func(self):
        '''
        A test that the current logged-in user must pass 
        to access the view- must be admin/teacher/student/parent
        '''
        user = self.request.user
        return is_admin(user) or is_teacher(user) or is_student(user) or is_parent(user)

    def get_queryset(self):
        '''
        Restrict students and parents to view of their own/their children's enrollment records
        '''
        user = self.request.user

        # For students
        if is_student(user):
            return Enrollment.objects.filter(student__user=user)
        # For parents
        elif is_parent(user):
            return Enrollment.objects.filter(student__parents__parent__user=user)
        # For teacher and admin
        else:
            return Enrollment.objects.all()

class EnrollmentDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    '''
    show details of a specific enrollment for a student
    Admin/Teacher can view all enrollments
    Students/Parents can see their own/their children's enrollment
    '''
    model = Enrollment
    template_name = 'records/enrollment_detail.html'
    context_object_name = 'enrollment'

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
            return Enrollment.objects.get(pk=pk, student__user=user)
        # For parents
        elif is_parent(user):
            return Enrollment.objects.get(pk=pk, student__parents__parent__user=user)
        # For admin and teachers
        return super().get_object()

class EnrollmentCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    '''allow admins to add new enrollment records'''
    model = Enrollment
    form_class = EnrollmentForm
    template_name = 'records/enrollment_create.html'
    success_url = reverse_lazy('enrollments')

    def test_func(self):
        '''A test that the current logged-in user must pass to access the view- must be admin'''
        return is_admin(self.request.user)

class EnrollmentUpdateView(LoginRequiredMixin, UserPassesTestMixin,UpdateView):
    '''enable admin to edit performance records'''
    model = Enrollment
    form_class = EnrollmentForm
    template_name = 'records/enrollment_update.html'
    success_url = reverse_lazy('enrollments')
    context_object_name = 'enrollment'

    def test_func(self):
        '''A test that the current logged-in user must pass to access the view- must be admin'''
        return is_admin(self.request.user)

class EnrollmentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    '''let admin delete enrollment records'''
    model = Enrollment
    template_name = 'records/enrollment_delete.html'
    success_url = reverse_lazy('enrollments')

    def test_func(self):
        '''A test that the current logged-in user must pass to access the view- must be admin'''
        return is_admin(self.request.user)
