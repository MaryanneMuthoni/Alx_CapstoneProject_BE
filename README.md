# Capstone project for the ALX Back End program

Create an API to manage a school records system where student details can be added which include personal information, academic information, financial information, contact information, teachers, classes, attendance, enrollment and parent/guardian information. The system will create, add, update and delete student records from the system.


<ins> **ERD Diagram with entities and relationships:** <ins>

<img width="1101" height="1150" alt="ERD 1 (4)" src="https://github.com/user-attachments/assets/ca030fef-26fd-49e2-b87a-a95222e99042" />

### Features

- CRUD operations for students
- Management of classes and enrollment
- Teacher information management
- Attendance tracking
- Academic performance recording
- Parent/guardian information storage
- Financial record handling (fees, payments)
- Endpoints for generating student reports
- Secure access using authentication 

### APIs
Create a custom REST API using Django REST Framework.

### Models and endpoints needed

1. **Student:**

ID, first_name, last_name, gender, date_of_birth, address, status, date_of_admission, class_id(ForeignkeyField linking with Class/Grade), student_email, profile_photo.

| Description | Method | Enpoint|
|-------------|--------|--------|
| Get all student records | GET | /students/ |
| Add a student |POST | /students/ |
| Get a particular student | GET | /students/<id> |
| Edit student record | PUT | /students/<id> |
| Delete student record | DELETE | /students/<id> |
| List student's enrollments | GET | /students/<id>/enrollments |
| List performance records | GET | /students/<id>/performance |
| Add performance for student |POST |/students/<id>/performance |
| List student attendance | GET | /students/<id>/attendance |
| List student invoice | GET | /students/<id>/invoices |


2. **Parent:**

ID, full_name, address, phone_number

| Description | Method | Enpoint|
|-------------|--------|--------|
| Get all parent records| GET | /parents/|
| Add a parent record | POST | /parents/ |
| Get a particular parent record | GET | /parents/<id> |
| Edit a parent record | PUT |/parents/<id> |
| Delete parent record | DELETE | /parents/<id> |
| Get children of a particular parent through StudentParent| GET | /parents/{id}/students/|


3. **StudentParent:**

This is a joint table between Student and Parent with the following fields: student_id(ForeignKey), parent_id(ForeignKey), relationship_type, is_primary_guardian.
Class/ Grade: ID, name, teacher_id(ForeignKeyField linking with Teacher), stream.

| Description | Method | Enpoint|
|-------------|--------|--------|
| Get all classes| GET | /classes/ |
| Create class | POST | /classes/ |
| Get a particular class record | GET | /classes/<id>/ |
| Update class record | PUT | /classes/<id>/
| Delete class record | DELETE | /classes/<id>/ |


4. **Teacher:**

ID, name, phone, email.

| Description | Method | Enpoint|
|-------------|--------|--------|
| Get all teacher records | GET | /teachers/ |
| Add a teacher | POST | /teachers/
| Get a particular teacher | GET |/teachers/<id> |
| Edit teacher record | PUT| /teachers/<id> |
| Delete teacher record | DELETE | /teachers/<id> |
| Get subjects teachers teach | GET | /teachers/<id>/subjects |
| Get classes teachers are class teachers of | GET | /teachers/<id>/classes |


5. **Subject:**

ID, name, teacher_id(Foreign Key linking with Teacher model)

| Description | Method | Enpoint|
|-------------|--------|--------|
| Get all subjects | GET | /subjects/ |
| Create subject entries | POST | /subjects/ |
| Get a particular subject | GET | /subjects/<id>/ |
| Update particular subject record | PUT | /subjects/<id>/ |
| Delete subject record | DELETE | /subjects/<id>/


6. **Performance:**

 ID, subject_id(Foreign Key linking with Subject),  score, exam_type, academic_year, term, student(Foreign Key linking with Student), date_entered.

| Description | Method | Enpoint|
|-------------|--------|--------|
| Get all performance records | GET | /performance/ |
| Add performance record| POST| /performance/ |
| Get particular performance record| GET| /performance/<id> |
| Update particular performance record| PUT| /performance/<id> |
| Delete particular performance record| DELETE| /performance/<id> |


7. **Attendance:**

ID, class_id(ForeignKey), student_id(Foreign Key linking with Student), status, date

| Description | Method | Enpoint|
|-------------|--------|--------|
| Get particular attendance record | GET | /attendance/{id}/ |
| Add attendance record | POST | /attendance/ |
| Get all attendance records | GET| /attendance/ |
| Update attendance record | PUT | /attendance/{id}/ |
| Delete attendance record | DELETE | /attendance/{id}/ |


8. **Invoices:**

ID, student_id(Foreign Key linking with Student), total_amount, amount_due, payment_due_date, status, term, academic_year.

| Description | Method | Enpoint|
|-------------|--------|--------|
| Get all invoices | GET | /invoices/ |
| Add invoice record| POST| /invoices/ |
| Get a particular invoice| GET| /invoices/{id}/ |
| Update a particular invoice| PUT| /invoices/{id}/ |
| Delete an invoice record| DELETE| /invoices/{id}/ |
| Get an invoice record from student table| GET | /students/{id}/invoices/ |


9. **Payments:**

ID, invoice_id(ForeignKey), amount_paid, payment_method, payment_date, reference_number

| Description | Method | Enpoint|
|-------------|--------|--------|
| Get all payment records| GET | /payments/ |
| Update existing payment record | POST| /payments/ |
| Get particular payment record | GET| /payments/<id> |


10. **Enrollment:**

ID, student_id(ForeignKey), class_id(ForeignKey), academic_year, date_enrolled, date_left, status.

| Description | Method | Enpoint|
|-------------|--------|--------|
| Get all enrollments | GET | /enrollments/|
| Get particular students enrollment | GET | /enrollments/{id}/ |
| Create new enrollment | POST |/enrollments/|
| Update particular enrollment | PUT | /enrollments/{id}/ |
| Delete particular enrollment | DELETE |/enrollments/{id}/ |

11. **Grade/Class:**
