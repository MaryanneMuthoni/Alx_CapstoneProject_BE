from django.shortcuts import render
from rest_framework import viewsets
from .models import from .models import Student, Parent, Grade, Teacher, Performance, Attendance, Invoice, Payment, Enrollment, Subject
from .serializers import StudeentSerializer, ParentSerializer, GradeSerializer, TeacherSerializer, PerformanceSerializer, AttendanceSerializer, InvoiceSerializer, PaymentSerializer, EnrollmentSerializer, SubjectSerializer

# Create your views here.
class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
