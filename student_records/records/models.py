from django.db import models

# Create your models here.
class Student(models.Model):
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=100, help_text='Enter first name')
    last_name = models.CharField(max_length=100, help_text='Enter last name')
    
    GENDER_CHOICES =[
            ('F', 'Female'),
            ('M', 'Male'),
            ('O', 'Other')
    ]

    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    date_of_birth = models.DateField()
    address = models.CharField(max_length=100)

    STATUS_CHOICES=[
            ('Enrolled', 'Student is enrolled'),
            ('Expelled', 'Student is expelled'),
            ('Suspended', 'Student is suspended'),
            ('Alumni', 'Student has completed'),
            ('Transferred', 'Student has transferred'),
    ]

    status = models.CharField(max_length=11, choices=STATUS_CHOICES)
    date_of_admission = models.DateField()
    class_id = models.ForeignKey(Class, on_delete=models.CASCADE)


class Parent(models.Model):
    id = models.AutoField(primary_key=True)
    full_name = models.CharField(max_length=100, help_text="Enter parent's full name")
    address = models.CharField(max_length=100)
    phone_number = models.IntegerField()


class StudentParent(models.Model):
    student_id = models.ForeignKey(Student, on_delete=models.CASCADE)
    parent = models.ForeignKey(Parent, on_delete=models.CASCADE)

    PRIMARY =[
            ('M', 'Mother'),
            ('F', 'Father'),
            ('G', 'Guardian'),
    ]

    relationship_type = models.CharField(max_length=1, choices=RELATIONSHIP_CHOICES)

    PRIMARY =[
            ('Y', 'Yes'),
            ('N', 'No'),
    ]

    is_primary_guardian = models.CharField(max_length=1, choices=PRIMARY)


class Class(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.IntegerField(help_text="Enter name of the class")
    stream = models.CharField(max_length=20,help_text="Enter stream name")
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)


class Teacher(models.Model):
    id = models.AutoField(primary_key=True)
    full_name = models.CharField(max_length=100, help_text="Enter teacher's full name")
    phone_number = models.IntegerField()
    email = models.EmailField()


class Subject(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.IntegerField(help_text="Enter name of the subject")
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)


class Performance(models.Model):
    id = models.AutoField(primary_key=True)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    score = models.IntegerField()

    EXAM_CHOICES =[
            ('CAT', 'Continous Assesment Test'),
            ('RAT', 'Random Assesment Test'),
            ('FINAL', 'Final Exam'),
    ]

    exam_type = models.CharField(max_length=5, choices=EXAM_CHOICES)
    academic_year = models.DateField()

    TERMS =[
            (1, 'One'),
            (2, 'Two'),
            (3, 'Three'),
    ]

    term = models.IntegerField(choices=TERMS)
    date_entered = models.DateField()


class Attendance(models.Model):
    id = models.AutoField(primary_key=True)
    class = models.ForeignKey(Class, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)

    STATUS_CHOICES =[
            (1, 'Present'),
            (0, 'Absent'),
    ]

    status= models.IntegerField(choices=STATUS_CHOICES)
    date = models.DateField()


class Invoice(models.Model):
    id = models.AutoField(primary_key=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    total_amount = models.DecimalField()
    amount_due = models.DecimalField()
    payment_due_date = models.DateField()

    PAYMENT_STATUS_CHOICES =[
            (1, 'Paid'),
            (0, 'Pending'),
    ]

    status = models.IntegerField(choices=PAYMENT_STATUS_CHOICES)
    academic_year = models.DateField()

    TERMS =[
            (1, 'One'),
            (2, 'Two'),
            (3, 'Three'),
    ]

    term = models.IntegerField(choices=TERMS)

class Payment(models.Model):
    id = models.AutoField(primary_key=True)
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    amount_paid = models.DecimalField()
    payment_method = models.CharField(max_length=50)
    payment_date =models.DateField()
    reference_number = models.IntegerField()


class Enrollment(models.Model):
    id = models.AutoField(primary_key=True)
    class = models.ForeignKey(Class, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    academic_year = models.DateField()
    date_enrolled = models.DateField()
    date_left = models.DateField()

    ENROLLMENT_STATUS_CHOICES =[
            (1, 'Enrolled'),
            (0, 'Not enrolled'),
    ]

    status = models.IntegerField(choices=ENROLLMENT_STATUS_CHOICES)
