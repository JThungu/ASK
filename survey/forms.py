from django import forms
from django.contrib.auth.models import User

from .models import Survey, Question, Option, UserProfile

class SurveyForm(forms.ModelForm):
    class Meta:
        model = Survey
        fields = ["title"]

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ["prompt"]

class OptionForm(forms.ModelForm):
    class Meta:
        model = Option
        fields = ["text"]

class AnswerForm(forms.Form):
    def __init__(self, *args, **kwargs):
        options = kwargs.pop("options")
        # Options must be a list of Option objects
        choices = {(o.pk, o.text) for o in options}
        super().__init__(*args, **kwargs)
        option_field = forms.ChoiceField(choices=choices, widget=forms.RadioSelect, required=True)
        self.fields["option"] = option_field

class BaseAnswerFormSet(forms.BaseFormSet):
    def get_form_kwargs(self, index):
        kwargs = super().get_form_kwargs(index)
        kwargs["options"] = kwargs["options"][index]
        return kwargs

# New UserProfileForm
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ["bio", "profile_picture", "date_of_birth", "location", "website"]

