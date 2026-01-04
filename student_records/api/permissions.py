from rest_framework.permissions import BasePermission
from records.views import is_admin, is_student, is_teacher, is_parent
from records.models import Teacher, Payment, Invoice

class AllRecordsPermission(BasePermission):
    """
    Handles all model permissions based on roles.
    Admin: All methods- view, update and delete all records for all models
    Teacher:['GET', 'HEAD', 'OPTIONS']- view all records from all models other than payment and invoice
    Student:['GET', 'HEAD', 'OPTIONS']- view only their own records for all models but all teacher records
    Parents:['GET', 'HEAD', 'OPTIONS']- view only their children's records from all models but all teacher records
    """

    def has_permission(self, request, view):
        '''Ensure user is logged in'''
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        '''Permission for specific records based on roles'''
        user = request.user
        method = request.method
        model_name = obj.__class__.__name__

        # For admin: full access
        if is_admin(user):
            return True

        # For student: can access their own records and Methods are GET, HEAD, OPTIONS
        if is_student(user):
            if hasattr(obj, 'student') and obj.student.user == user:
                '''Indirect relationship'''
                return method in ['GET', 'HEAD', 'OPTIONS']
            elif hasattr(obj, 'user') and obj.user == user:
                '''Direct relationship- student object itself'''
                return method in ['GET', 'HEAD', 'OPTIONS']
            elif isinstance(obj, Teacher):
                '''Allow students to see all Teacher records'''
                return method in ['GET', 'HEAD', 'OPTIONS']
            else:
                return False


        # For parents: can access their own records and own children's records, Methods are GET, HEAD, OPTIONS
        if is_parent(user):
            if hasattr(obj, 'student') and obj.student.parents.filter(parent__user=user).exists():
                '''Indirect relationship'''
                return method in ['GET', 'HEAD', 'OPTIONS']
            elif hasattr(obj, 'user') and obj.user == user:
                '''Direct relationship- parent object itself'''
                return method in ['GET', 'HEAD', 'OPTIONS']
            elif isinstance(obj, Teacher):
                '''Allow parents to see all Teacher records'''
                return method in ['GET', 'HEAD', 'OPTIONS']
            else:
                return False


        # For teachers: can access their own records, all student records other than Invoice and Payment
        # Methods are GET, HEAD, OPTIONS
        if is_teacher(user):
            if isinstance(obj, (Payment, Invoice)):
                return False
            elif hasattr(obj, 'user') and obj.user == user:
                '''Direct relationship- teacher object itself'''
                return method in ['GET', 'HEAD', 'OPTIONS']
            else:
                return method in ['GET', 'HEAD', 'OPTIONS']

        # default if does not meet authentication and permissions
        return False
