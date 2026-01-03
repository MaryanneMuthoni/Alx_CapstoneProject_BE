from django.shortcuts import render
from rest_framework import viewsets
from .models import from .models import Student, Parent, Grade, Teacher, Performance, Attendance, Invoice, Payment, Enrollment, Subject
from .serializers import StudeentSerializer, ParentSerializer, GradeSerializer, TeacherSerializer, PerformanceSerializer, AttendanceSerializer, InvoiceSerializer, PaymentSerializer, EnrollmentSerializer, SubjectSerializer

# Create your views here.

# DRF ViewSet views- do all CRUD operations
# =========================================
# Student ViewSet view
class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

# Parent ViewSet view
class ParentViewSet(viewsets.ModelViewSet):
    queryset = Parent.objects.all()
    serializer_class = ParentSerializer

# Grade ViewSet view
class GradeViewSet(viewsets.ModelViewSet):
    queryset = Grade.objects.all()
    serializer_class = GradeSerializer

# Subject ViewSet view
class SubjectViewSet(viewsets.ModelViewSet):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer

# Teacher ViewSet view
class TeacherViewSet(viewsets.ModelViewSet):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer

# Performance ViewSet view
class PerformanceViewSet(viewsets.ModelViewSet):
    queryset = Performance.objects.all()
    serializer_class = PerformanceSerializer

# Attendance ViewSet view
class AttendanceViewSet(viewsets.ModelViewSet):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer

# Invoice ViewSet view
class InvoiceViewSet(viewsets.ModelViewSet):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer

# Payment ViewSet view
class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

# Enrollment ViewSet view
class EnrollmentViewSet(viewsets.ModelViewSet):
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer
