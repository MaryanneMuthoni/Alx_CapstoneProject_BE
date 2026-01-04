from django.shortcuts import render
from rest_framework import viewsets
from .models import from .models import Student, Parent, Grade, Teacher, Performance, Attendance, Invoice, Payment, Enrollment, Subject
from .serializers import StudentSerializer, ParentSerializer, GradeSerializer, TeacherSerializer, PerformanceSerializer, AttendanceSerializer, InvoiceSerializer, PaymentSerializer, EnrollmentSerializer, SubjectSerializer
from .permissions import AllRecordsPermission
from records.views import is_admin, is_student, is_teacher, is_parent
from rest_framework.permissions import IsAuthenticated

# Create your views here.

# DRF ViewSet views- do all CRUD operations
# =========================================
# Student ViewSet view
class StudentViewSet(viewsets.ModelViewSet):
    serializer_class = StudentSerializer
    permission_classes = [IsAuthenticated, AllRecordsPermission]

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
        elif is_admin(user) or is_teacher(user):
            return Student.objects.all()
        else:
            return Student.objects.none()


# Parent ViewSet view
class ParentViewSet(viewsets.ModelViewSet):
    serializer_class = ParentSerializer
    permission_classes = [IsAuthenticated, AllRecordsPermission]
    
    def get_queryset(self):
        '''Restrict parents/students to view of their own/their parent's records'''
        user = self.request.user

        # For students
        if is_student(user):
            return Parent.objects.filter(user=user)
        # For parents
        elif is_parent(user):
            return Parent.objects.filter(students__student__user=user)
        # For teacher and admin
        elif is_teacher(user) or is_admin(user):
            return Parent.objects.all()
        else:
            return Parent.objects.none()


# Grade ViewSet view
class GradeViewSet(viewsets.ModelViewSet):
    serializer_class = GradeSerializer
    permission_classes = [IsAuthenticated, AllRecordsPermission]

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
        elif is_teacher(user) or is_admin(user):
            return Grade.objects.all()
        else:
            return Parent.objects.none()


# Subject ViewSet view
class SubjectViewSet(viewsets.ModelViewSet):
    serializer_class = SubjectSerializer
    permission_classes = [IsAuthenticated, AllRecordsPermission]

    def get_queryset(self):
        '''All roles can see Subject model information'''
        return Subject.objects.all()


# Teacher ViewSet view
class TeacherViewSet(viewsets.ModelViewSet):
    serializer_class = TeacherSerializer
    permission_classes = [IsAuthenticated, AllRecordsPermission]

    def get_queryset(self):
        '''All roles can see Teacher model information'''
        return Teacher.objects.all()


# Performance ViewSet view
class PerformanceViewSet(viewsets.ModelViewSet):
    serializer_class = PerformanceSerializer
    permission_classes = [IsAuthenticated, AllRecordsPermission]
    
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
        elif is_teacher(user) or is_admin(user):
            return Performance.objects.all()
        else:
            return Performance.objects.none()
            

# Attendance ViewSet view
class AttendanceViewSet(viewsets.ModelViewSet):
    serializer_class = AttendanceSerializer
    permission_classes = [IsAuthenticated, AllRecordsPermission]

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
        elif is_teacher(user) or is_admin(user):
            return Attendance.objects.all()
        else:
            return Attendance.objects.none()


# Invoice ViewSet view
class InvoiceViewSet(viewsets.ModelViewSet):
    serializer_class = InvoiceSerializer
    permission_classes = [IsAuthenticated, AllRecordsPermission]

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
        elif is_admin(user):
            return Invoice.objects.all()
        else:
            return Invoice.objects.none()


# Payment ViewSet view
class PaymentViewSet(viewsets.ModelViewSet):
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated, AllRecordsPermission]

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
        elif is_admin(user):
            return Payment.objects.all()
        else:
            return Payment.objects.none()

# Enrollment ViewSet view
class EnrollmentViewSet(viewsets.ModelViewSet):
    serializer_class = EnrollmentSerializer
    permission_classes = [IsAuthenticated, AllRecordsPermission]

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
        elif is_teacher(user) or is_admin(user):
            return Enrollment.objects.all()
        else:
            return Enrollment.objects.none()
