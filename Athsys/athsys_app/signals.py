#Import methods to be used
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.contrib.auth import user_logged_in
from django.utils import timezone
from .models import *

#The signal is emitted after creating a user to perform an action.
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
#The signal is emitted after logging in to perform an action.
@receiver(user_logged_in)
def register_user_login(sender, request, user, **kwargs):
    EventLogin.objects.create(user = user, timestamp = timezone.now())