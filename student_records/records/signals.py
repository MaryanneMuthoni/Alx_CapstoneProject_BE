# relationship_app/signals.py
# to autocreate UserProfile when new user is registered
# Defaults role to pending, waiting for approval and role assignment

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import UserProfile


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance, role="Pending")
