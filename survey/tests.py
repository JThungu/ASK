from django.contrib.auth.views import LoginView
from .views.auth import signup
from django.test import TestCase
from django.urls import reverse
from survey.views.landing import LandingView
from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView as BaseLoginView
from django.contrib.auth.models import User
from django.utils import timezone
from .models import UserProfile, Survey, Question, Option, Submission, Answer
from .forms import SurveyForm, QuestionForm, OptionForm, AnswerForm, UserProfileForm
from survey.models import Survey, UserProfile, Question, Option, Submission, Answer
from survey.views.survey import (
    export_results_csv,
    create_profile,
    survey_list,
    detail,
    create,
    delete,
    edit,
    question_create,
    option_create,
    start,
    submit,
    thanks,
)


class AuthViewsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", email="test@example.com", password="testpassword"
        )
        self.user_profile = UserProfile.objects.create(user=self.user)

    def test_login_view_get(self):
        response = self.client.get(reverse("account_login"))
        self.assertEqual(response.status_code, 200)

    def test_login_view_post_invalid_credentials(self):
        data = {"login": self.user.username, "password": "wrongpassword"}
        response = self.client.post(reverse("account_login"), data)
        self.assertEqual(response.status_code, 200)

    def test_login_view_post_valid_credentials(self):
        data = {"login": self.user.username, "password": "testpassword"}
        response = self.client.post(reverse("account_login"), data)

    def test_signup_view_get(self):
        response = self.client.get(reverse("account_signup"))
        self.assertEqual(response.status_code, 200)

    def test_signup_view_post_invalid_data(self):
        data = {"username": "", "email": "invalidemail", "password1": "pass", "password2": "pass"}
        response = self.client.post(reverse("account_signup"), data)
        self.assertEqual(response.status_code, 200)

    def test_signup_view_post_valid_data(self):
        data = {"username": "newuser", "email": "newuser@example.com", "password1": "testpassword", "password2": "testpassword"}
        response = self.client.post(reverse("account_signup"), data)
        self.assertEqual(response.status_code, 302)


class ModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", email="test@example.com", password="testpassword"
        )
        self.user_profile = UserProfile.objects.create(user=self.user)
        self.survey = Survey.objects.create(title="Test Survey", creator=self.user_profile)
        self.question = Question.objects.create(survey=self.survey, prompt="Test Question")
        self.option = Option.objects.create(question=self.question, text="Option 1")

    def test_option_string_representation(self):
        self.assertEqual(str(self.option), "Option 1")

    def test_question_string_representation(self):
        self.assertEqual(str(self.question), "Test Question")


class FormTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", email="test@example.com", password="testpassword"
        )
        self.user_profile = UserProfile.objects.create(user=self.user)
        self.survey = Survey.objects.create(title="Test Survey", creator=self.user_profile)
        self.question = Question.objects.create(survey=self.survey, prompt="Test Question")
        self.option1 = Option.objects.create(question=self.question, text="Option 1")
        self.option2 = Option.objects.create(question=self.question, text="Option 2")

