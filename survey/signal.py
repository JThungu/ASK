from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import UserProfile

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        # User is newly created, create a UserProfile instance
        UserProfile.objects.create(user=instance)
    else:
        # User already exists, update the UserProfile instance
        instance.userprofile.save()

