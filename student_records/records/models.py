from django.db import models

# Create your models here.
class Student(models.Model):
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=100, help_text='Enter first name', blank=False)
    last_name = models.CharField(max_length=100, help_text='Enter last name', blank=False)
    
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
    student_email = models.EmailField(unique=True, blank=True)
    profile_photo = models.ImageField(upload_to="students/", null=True, blank=True)
    grade = models.ForeignKey("Grade", on_delete=models.SET_NULL, null=True, related_name="students")

    class Meta:
        '''Default order and name for model in admin and forms'''
        ordering=['first_name', 'last_name']
        verbose_name='Student details'

    def __str__(self):
        return f'Student: {self.first_name} {self.last_name}'


# Parent table/model
class Parent(models.Model):
    '''Class that defines parent instance attributes'''
    id = models.AutoField(primary_key=True)
    full_name = models.CharField(max_length=100, help_text="Enter parent's full name")
    address = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=13, unique=True)
    email = models.EmailField(null=True, blank=True)

    class Meta:
        '''Default order and name for model in admin and forms'''
        ordering=['full_name']
        verbose_name='Parent details'

    def __str__(self):
        return f'Parent: {self.full_name}'


# Join table for Parent and Student table
class StudentParent(models.Model):
    '''Class that defines studentparent instance attributes'''
    student = models.ForeignKey(Student, on_delete=models.CASCADE, null=True, related_name="parents")
    parent = models.ForeignKey(Parent, on_delete=models.CASCADE, related_name="students")

    RELATIONSHIP_CHOICES = [
            ('M', 'Mother'),
            ('F', 'Father'),
            ('G', 'Guardian'),
    ]

    relationship_type = models.CharField(max_length=1, choices=RELATIONSHIP_CHOICES)
    is_primary_guardian = models.BooleanField(default=False)
    
    class Meta:
        '''Name for model in admin and forms'''
        verbose_name='Student-Parent join table'

# Grade/Class table/model
class Grade(models.Model):
    '''Class that defines grade/class instance attributes'''
    id = models.AutoField(primary_key=True)
    name = models.IntegerField(help_text="Enter name of the class")
    stream = models.CharField(max_length=20,help_text="Enter stream name")
    teacher = models.ForeignKey("Teacher", on_delete=models.SET_NULL, null=True, related_name="classes")

    class Meta:
        '''Default order and name for model in admin and forms'''
        ordering=['name']
        verbose_name='Class details'

    def __str__(self):
        return f'Grade: {self.name} {self.stream}'


# Teacher table/model
class Teacher(models.Model):
    '''Class that defines teacher instance attributes'''
    id = models.AutoField(primary_key=True)
    full_name = models.CharField(max_length=100, help_text="Enter teacher's full name")
    phone_number = models.CharField(max_length=13, unique=True)
    email = models.EmailField(unique=True, blank=True)

    class Meta:
        '''Default order and name for model in admin and forms'''
        ordering=['full_name']
        verbose_name='Teacher details'

    def __str__(self):
        return f'Teacher: {self.full_name}'


# Subject table/model
class Subject(models.Model):
    '''Class that defines subject instance attributes'''
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, help_text="Enter name of the subject")
    teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, related_name="subjects")

    class Meta:
        '''Default order and name for model in admin and forms'''
        ordering=['name']
        verbose_name='Subject details'

    def __str__(self):
        return f'Subject: {self.name}'


# Performance table/model
class Performance(models.Model):
    '''Class that defines performance instance attributes'''
    id = models.AutoField(primary_key=True)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name="performance")
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="performance")
    score = models.IntegerField()

    EXAM_CHOICES =[
            ('CAT', 'Continous Assesment Test'),
            ('RAT', 'Random Assesment Test'),
            ('FINAL', 'Final Exam'),
    ]

    exam_type = models.CharField(max_length=5, choices=EXAM_CHOICES)
    academic_year = models.IntegerField()

    TERMS =[
            (1, 'One'),
            (2, 'Two'),
            (3, 'Three'),
    ]

    term = models.IntegerField(choices=TERMS)
    date_entered = models.DateField(auto_now_add=True)

    class Meta:
        '''Default order and name for model in admin and forms'''
        ordering=['academic_year', 'term']
        verbose_name='Exam details'

# Attendance model/table
class Attendance(models.Model):
    '''Class that defines attendance instance attributes'''
    id = models.AutoField(primary_key=True)
    grade = models.ForeignKey(Grade, on_delete=models.CASCADE, related_name="attendance")
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="attendance")

    STATUS_CHOICES =[
            (1, 'Present'),
            (0, 'Absent'),
    ]

    status= models.IntegerField(choices=STATUS_CHOICES)
    date = models.DateField()


# Invoice table/model
class Invoice(models.Model):
    '''Class that defines invoice instance attributes'''
    id = models.AutoField(primary_key=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="invoices")
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    amount_due = models.DecimalField(max_digits=10, decimal_places=2)
    payment_due_date = models.DateField()

    PAYMENT_STATUS_CHOICES =[
            ('PAID', 'Paid'),
            ('PENDING', 'Pending'),
    ]

    status = models.CharField(max_length=10, choices=PAYMENT_STATUS_CHOICES)
    academic_year = models.IntegerField()

    TERMS =[
            (1, 'One'),
            (2, 'Two'),
            (3, 'Three'),
    ]

    term = models.IntegerField(choices=TERMS)

    class Meta:
        '''Default order'''
        ordering=['academic_year', 'term']


# Payment table/model
class Payment(models.Model):
    '''Class that defines payment instance attributes'''
    id = models.AutoField(primary_key=True)
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name="payments")
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=50)
    payment_date =models.DateField()
    reference_number = models.CharField(max_length=100)

    class Meta:
        '''Default order'''
        ordering=['payment_date']


# Enrollment table/model
class Enrollment(models.Model):
    '''Class that defines enrollment instance attributes'''
    id = models.AutoField(primary_key=True)
    grade = models.ForeignKey(Grade, on_delete=models.CASCADE, related_name="enrollments")
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="enrollments")
    academic_year = models.IntegerField()
    date_enrolled = models.DateField()
    date_left = models.DateField(null=True, blank=True)

    ENROLLMENT_STATUS_CHOICES =[
            ('ENROLLED', 'Enrolled'),
            ('LEFT', 'Not enrolled'),
    ]

    status = models.CharField(max_length=10, choices=ENROLLMENT_STATUS_CHOICES)

    class Meta:
        '''Default order'''
        ordering=['date_enrolled']
