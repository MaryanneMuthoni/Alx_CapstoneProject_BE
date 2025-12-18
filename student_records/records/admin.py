from django.contrib import admin
from .models import Grade, Invoice, Parent, Subject, Teacher, Payment, Enrollment, Attendance, StudentParent, Performance, Student

class StudentAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'gender', 'date_of_birth',  'status')

# Register your models here.
admin.site.register(Student, StudentAdmin)
admin.site.register(Parent)
admin.site.register(StudentParent)
admin.site.register(Teacher)
admin.site.register(Subject)
admin.site.register(Performance)
admin.site.register(Attendance)
admin.site.register(Invoice)
admin.site.register(Payment)
admin.site.register(Enrollment)
admin.site.register(Grade)
