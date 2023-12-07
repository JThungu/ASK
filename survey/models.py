from django.contrib.auth.models import AbstractUser, User
from django.db import models
from django.utils import timezone

class CustomUser(AbstractUser):
    """user email verification"""
    email_verified = models.BooleanField(default=False)

    class Meta:
        # Add unique related_name arguments to avoid clashes
        abstract = False  # Set abstract to False to avoid system check errors
        swappable = 'AUTH_USER_MODEL'
        unique_together = ('email_verified',)

CustomUser._meta.get_field('groups').related_query_name = 'custom_user_groups'
CustomUser._meta.get_field('user_permissions').related_query_name = 'custom_user_permissions'

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

