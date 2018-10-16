from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, timedelta
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='profilepics')
    credits = models.IntegerField(default=0)

    def is_active_subscriber(self):
        if self.user.subscription is not None:
            return not self.user.subscription.is_expired
        else:
            return False


    def __str__(self):
        return self.user.username

def get_expiration_date():
    return datetime.today() + timedelta(days=365)

class Subscription(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    expires = models.DateTimeField(default=get_expiration_date)

    @property
    def is_expired(self):
        return timezone.now() > self.expires
    
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
