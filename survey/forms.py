from .models import Survey, Question, Option

from django import forms


class SurveyForm(forms.ModelForm):
    """
    Form for creating or updating a survey.
    """
    class Meta:
        model = Survey
        fields = ["title"]


class QuestionForm(forms.ModelForm):
    """
    Form for creating or updating a question in a survey.
    """
    class Meta:
        model = Question
        fields = ["prompt"]


class OptionForm(forms.ModelForm):
    """
    Form for creating or updating a multi-choice option in a survey question.
    """
    class Meta:
        model = Option
        fields = ["text"]


class AnswerForm(forms.Form):
    """
    Form for providing an answer to a survey question.
    """
    def __init__(self, *args, **kwargs):
        options = kwargs.pop("options")
        # Options must be a list of Option objects
        choices = [(o.pk, o.text) for o in options]
        super().__init__(*args, **kwargs)
        option_field = forms.ChoiceField(choices=choices, widget=forms.RadioSelect, required=True)
        self.fields["option"] = option_field


class BaseAnswerFormSet(forms.BaseFormSet):
    """
    Base formset for handling answers to survey questions.
    """
    def get_form_kwargs(self, index):
        kwargs = super().get_form_kwargs(index)
        kwargs["options"] = kwargs["options"][index]
        return kwargs
