#Import methods to be used
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

#Data model for the Profile table
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='avatar.png')
    
    def __str__(self):
        return f'Perfil: {self.user.username}'

#Data model for the eventlogin table
class EventLogin(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='eventlogin')
    timestamp = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f'{self.user.username}: {self.timestamp}'