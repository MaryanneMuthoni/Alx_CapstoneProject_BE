from django import forms
from .models import Student

class StudentForm(forms.ModelForm):
    '''Form to handle the creation and updating of student records'''
    class Meta:
        model = Student
        fields = ('first_name', 'last_name', 'gender', 'date_of_birth', 'address', 
                'status', 'date_of_admission', 'student_email', 'profile_photo')
