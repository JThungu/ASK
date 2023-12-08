from django.utils import timezone
from django.contrib.auth.models import User
from django.db import models

#class UserProfile(models.Model):
#    """user profile"""
#    user = models.OneToOneField(User, on_delete=models.CASCADE)
#    bio = models.TextField(blank=True, null=True)
#    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
#    date_of_birth = models.DateField(blank=True, null=True)
#    location = models.CharField(max_length=255, blank=True, null=True)
#    website = models.URLField(blank=True, null=True)
#    created_at = models.DateTimeField(default=timezone.now)
#
#    def __str__(self):
#        return self.user.username

class Survey(models.Model):
    """A survey created by a user."""

    title = models.CharField(max_length=64)
    is_active = models.BooleanField(default=False)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)


class Question(models.Model):
    """A question in a survey"""

    survey = models.ForeignKey(Survey, on_delete=models.CASCADE)
    prompt = models.CharField(max_length=128)


class Option(models.Model):
    """A multi-choice option available as a part of a survey question."""

    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.CharField(max_length=128)


class Submission(models.Model):
    """A set of answers a survey's questions."""

    survey = models.ForeignKey(Survey, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    is_complete = models.BooleanField(default=False)


class Answer(models.Model):
    """An answer a survey's questions."""

    submission = models.ForeignKey(Submission, on_delete=models.CASCADE)
    option = models.ForeignKey(Option, on_delete=models.CASCADE)
