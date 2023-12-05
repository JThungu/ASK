from django.contrib.auth.models import User
from django.utils import timezone
from django.db import models

class Survey(models.Model):
    """
    A survey created by a user.
    """
    title = models.CharField(max_length=64)
    is_active = models.BooleanField(default=False)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


class Question(models.Model):
    """
    A question in a survey.
    """
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE, related_name='questions')
    prompt = models.CharField(max_length=128)


class Option(models.Model):
    """
    A multi-choice option available as a part of a survey question.
    """
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='options')
    text = models.CharField(max_length=128)


class Submission(models.Model):
    """
    A set of answers to a survey's questions.
    """
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE, related_name='submissions')
    created_at = models.DateTimeField(auto_now_add=True)
    is_complete = models.BooleanField(default=False)


class Answer(models.Model):
    """
    An answer to a survey's questions.
    """
    submission = models.ForeignKey(Submission, on_delete=models.CASCADE, related_name='answers')
    option = models.ForeignKey(Option, on_delete=models.CASCADE)

