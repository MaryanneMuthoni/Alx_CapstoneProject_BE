# records/urls.py
from django.urls import path
from .views import admin_view, student_view, teacher_view, parent_view, pending_view, login_redirect, StudentListView, StudentDetailView, StudentCreateView, StudentUpdateView, StudentDeleteView, ParentListView, ParentDetailView, ParentCreateView, ParentUpdateView, ParentDeleteView, GradeListView, GradeDetailView, GradeCreateView, GradeUpdateView, GradeDeleteView, TeacherListView, TeacherDetailView, TeacherCreateView, TeacherUpdateView, TeacherDeleteView, SubjectListView, SubjectDetailView, SubjectCreateView, SubjectUpdateView, SubjectDeleteView, PerformanceListView, PerformanceDetailView, PerformanceCreateView, PerformanceUpdateView, PerformanceDeleteView, AttendanceListView, AttendanceDetailView, AttendanceCreateView, AttendanceUpdateView, AttendanceDeleteView, InvoiceListView, InvoiceDetailView, InvoiceCreateView, InvoiceUpdateView, InvoiceDeleteView, PaymentListView, PaymentDetailView, PaymentCreateView, PaymentUpdateView, PaymentDeleteView, EnrollmentListView, EnrollmentDetailView, EnrollmentCreateView, EnrollmentUpdateView, EnrollmentDeleteView

urlpatterns = [
    # Role views url mapping
    path('admin_view/', admin_view, name='admin_view'),
    path('student_view/', student_view, name='student_view'),
    path('teacher_view/', teacher_view, name='teacher_view'),
    path('parent_view/', parent_view, name='parent_view'),
    path('pending/', pending_view, name='pending_view'),
    path('login_redirect/', login_redirect, name='login_redirect'),
    # student model CRUD views url mapping
    path('students/', StudentListView.as_view(), name='student_list'),
    path('student/<int:pk>/', StudentDetailView.as_view(), name='student_detail'),
    path('student/new/', StudentCreateView.as_view(), name='student_create'),
    path('student/<int:pk>/update/', StudentUpdateView.as_view(), name='student_update'),
    path('student/<int:pk>/delete/', StudentDeleteView.as_view(), name='student_delete'),
    # parent model CRUD views url mapping
    path('parents/', ParentListView.as_view(), name='parent_list'),
    path('parent/<int:pk>/', ParentDetailView.as_view(), name='parent_detail'),
    path('parent/new/', ParentCreateView.as_view(), name='parent_create'),
    path('parent/<int:pk>/update/', ParentUpdateView.as_view(), name='parent_update'),
    path('parent/<int:pk>/delete/', ParentDeleteView.as_view(), name='parent_delete'),
    # grade model CRUD views url mapping
    path('grades/', GradeListView.as_view(), name='grade_list'),
    path('grade/<int:pk>/', GradeDetailView.as_view(), name='grade_detail'),
    path('grade/new/', GradeCreateView.as_view(), name='grade_create'),
    path('grade/<int:pk>/update/', GradeUpdateView.as_view(), name='grade_update'),
    path('grade/<int:pk>/delete/', GradeDeleteView.as_view(), name='grade_delete'),
    # teacher model CRUD views url mapping
    path('teachers/', TeacherListView.as_view(), name='teacher_list'),
    path('teacher/<int:pk>/', TeacherDetailView.as_view(), name='teacher_detail'),
    path('teacher/new/', TeacherCreateView.as_view(), name='teacher_create'),
    path('teacher/<int:pk>/update/', TeacherUpdateView.as_view(), name='teacher_update'),
    path('teacher/<int:pk>/delete/', TeacherDeleteView.as_view(), name='teacher_delete'),
    # subject model CRUD views url mapping
    path('subjects/', SubjectListView.as_view(), name='subject_list'),
    path('subject/<int:pk>/', SubjectDetailView.as_view(), name='subject_detail'),
    path('subject/new/', SubjectCreateView.as_view(), name='subject_create'),
    path('subject/<int:pk>/update/', SubjectUpdateView.as_view(), name='subject_update'),
    path('subject/<int:pk>/delete/', SubjectDeleteView.as_view(), name='subject_delete'),
    # performance model CRUD views url mapping
    path('performances/', PerformanceListView.as_view(), name='performance_list'),
    path('performance/<int:pk>/', PerformanceDetailView.as_view(), name='performance_detail'),
    path('performance/new/', PerformanceCreateView.as_view(), name='performance_create'),
    path('performance/<int:pk>/update/', PerformanceUpdateView.as_view(), name='performance_update'),
    path('performance/<int:pk>/delete/', PerformanceDeleteView.as_view(), name='performance_delete'),
    # attendance model CRUD views url mapping
    path('attendances/', AttendanceListView.as_view(), name='attendance_list'),
    path('attendance/<int:pk>/', AttendanceDetailView.as_view(), name='attendance_detail'),
    path('attendance/new/', AttendanceCreateView.as_view(), name='attendance_create'),
    path('attendance/<int:pk>/update/', AttendanceUpdateView.as_view(), name='attendance_update'),
    path('attendance/<int:pk>/delete/', AttendanceDeleteView.as_view(), name='attendance_delete'),
    # invoice model CRUD views url mapping
    path('invoices/', InvoiceListView.as_view(), name='invoice_list'),
    path('invoice/<int:pk>/', InvoiceDetailView.as_view(), name='invoice_detail'),
    path('invoice/new/', InvoiceCreateView.as_view(), name='invoice_create'),
    path('invoice/<int:pk>/update/', InvoiceUpdateView.as_view(), name='invoice_update'),
    path('invoice/<int:pk>/delete/', InvoiceDeleteView.as_view(), name='invoice_delete'),
    # payment model CRUD views url mapping
    path('payments/', PaymentListView.as_view(), name='payment_list'),
    path('payment/<int:pk>/', PaymentDetailView.as_view(), name='payment_detail'),
    path('payment/new/', PaymentCreateView.as_view(), name='payment_create'),
    path('payment/<int:pk>/update/', PaymentUpdateView.as_view(), name='payment_update'),
    path('payment/<int:pk>/delete/', PaymentDeleteView.as_view(), name='payment_delete'),
    # enrollment model CRUD views url mapping
    path('enrollments/', EnrollmentListView.as_view(), name='enrollment_list'),
    path('enrollment/<int:pk>/', EnrollmentDetailView.as_view(), name='enrollment_detail'),
    path('enrollment/new/', EnrollmentCreateView.as_view(), name='enrollment_create'),
    path('enrollment/<int:pk>/update/', EnrollmentUpdateView.as_view(), name='enrollment_update'),
    path('enrollment/<int:pk>/delete/', EnrollmentDeleteView.as_view(), name='enrollment_delete'),
]
