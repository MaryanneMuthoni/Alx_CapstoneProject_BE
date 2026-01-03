from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import StudentViewSet, ParentViewSet, GradeViewSet, SubjectViewSet, TeacherViewSet, PerformanceViewSet, AttendanceViewSet, InvoiceViewSet, PaymentViewSet, PerformanceViewSet, EnrollmentViewSet

router = DefaultRouter()
router.register(r'students', StudentViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]
