from django import forms
from .models import Student, Parent, Grade, Teacher, Subject, Performance, Attendance, Enrollment, Payment, Invoice

class StudentForm(forms.ModelForm):
    '''Form to handle the creation and updating of student records'''
    class Meta:
        model = Student
        fields = ('first_name', 'last_name', 'gender', 'date_of_birth', 'address', 
                'status', 'date_of_admission', 'grade',)

class ParentForm(forms.ModelForm):
    '''Form to handle the creation and updating of parent records'''
    class Meta:
        model = Parent
        fields = ('full_name', 'address')

class GradeForm(forms.ModelForm):
    '''Form to handle the creation and updating of grade records'''
    class Meta:
        model = Grade
        fields = ('name', 'stream')

class TeacherForm(forms.ModelForm):
    '''Form to handle the creation and updating of teacher records'''
    class Meta:
        model = Teacher
        fields = ('full_name',)

class SubjectForm(forms.ModelForm):
    '''Form to handle the creation and updating of subject records'''
    class Meta:
        model = Subject
        fields = ('name', 'teacher')

class PerformanceForm(forms.ModelForm):
    '''Form to handle the creation and updating of performance records'''
    class Meta:
        model = Performance
        fields = ('subject', 'score', 'exam_type', 'academic_year', 'term')

class PaymentForm(forms.ModelForm):
    '''Form to handle the creation and updating of payment records'''
    class Meta:
        model = Payment
        fields = ('amount_paid', 'payment_method', 'payment_date', 'reference_number')

class InvoiceForm(forms.ModelForm):
    '''Form to handle the creation and updating of invoice records'''
    class Meta:
        model = Invoice
        fields = ('total_amount', 'amount_due', 'payment_due_date', 'status', 'academic_year', 'term')

class AttendanceForm(forms.ModelForm):
    '''Form to handle the creation and updating of attendance records'''
    class Meta:
        model = Attendance
        fields = ('grade', 'status', 'date')

class EnrollmentForm(forms.ModelForm):
    '''Form to handle the creation and updating of enrollment records'''
    class Meta:
        model = Enrollment
        fields = ('grade', 'academic_year', 'date_enrolled', 'date_left', 'status')
