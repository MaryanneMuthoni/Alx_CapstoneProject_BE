from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class CustomUser(AbstractUser):
    '''
    Extend default User model to have extra fields in addition
    to the default ones: username, email, and password
    '''
    profile_picture  = models.ImageField(upload_to="profiles/", null=True, blank=True)
    phone_number = models.CharField(max_length=13, unique=True)
