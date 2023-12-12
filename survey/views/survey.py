from django.http import HttpResponse
from django.db import transaction
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.forms.formsets import formset_factory
from ..models import Survey, UserProfile, Question, Answer, Submission
from ..forms import SurveyForm, UserProfileForm, QuestionForm, OptionForm, AnswerForm, BaseAnswerFormSet

@login_required
def create_profile(request):
    try:
        # Check if the user already has a profile
        user_profile = UserProfile.objects.get(user=request.user)
        return redirect("survey-list")
    except UserProfile.DoesNotExist:
        # If the user doesn't have a profile, process the profile creation form
        if request.method == "POST":
            form = UserProfileForm(request.POST, request.FILES)
            if form.is_valid():
                # Save the profile and associate it with the user
                user_profile = form.save(commit=False)
                user_profile.user = request.user
                user_profile.save()
                return redirect("survey-list")
        else:
            form = UserProfileForm()

        return render(request, 'survey/create_profile.html', {'form': form})

@login_required
def survey_list(request):
    """User can view all their surveys"""
    try:
        user_profile = UserProfile.objects.get(user=request.user)
        surveys = Survey.objects.filter(creator=user_profile).order_by("-created_at").all()
        return render(request, "survey/list.html", {"surveys": surveys})
    except UserProfile.DoesNotExist:
        # Handle the case where UserProfile does not exist for the current user
        return redirect(reverse("create-profile"))

@login_required
def detail(request, pk):
    """User can view an active survey"""
    try:
        survey = Survey.objects.prefetch_related("question_set__option_set").get(
            pk=pk, creator=request.user.userprofile, is_active=True
        )
    except Survey.DoesNotExist:
        raise Http404()

    questions = survey.question_set.all()

    for question in questions:
        option_pks = question.option_set.values_list("pk", flat=True)
        total_answers = Answer.objects.filter(option_id__in=option_pks).count()
        for option in question.option_set.all():
            num_answers = Answer.objects.filter(option=option).count()
            option.percent = 100.0 * num_answers / total_answers if total_answers else 0

    host = request.get_host()
    public_path = reverse("survey-start", args=[pk])
    public_url = f"{request.scheme}://{host}{public_path}"
    num_submissions = survey.submission_set.filter(is_complete=True).count()
    return render(
        request,
        "survey/detail.html",
        {
            "survey": survey,
            "public_url": public_url,
            "questions": questions,
            "num_submissions": num_submissions,
        },
    )


@login_required
def create(request):
    """User can create a new survey"""
    if request.method == "POST":
        form = SurveyForm(request.POST)
        if form.is_valid():
            survey = form.save(commit=False)

            # Get or create UserProfile instance for the current user
            user_profile, created = UserProfile.objects.get_or_create(user=request.user)

            # Assign UserProfile instance to the Survey.creator field
            survey.creator = user_profile
            survey.save()

            return redirect("survey-edit", pk=survey.id)
    else:
        form = SurveyForm()

    return render(request, "survey/create.html", {"form": form})


@login_required
def delete(request, pk):
    """User can delete an existing survey"""
    survey = get_object_or_404(Survey, pk=pk, creator=request.user.userprofile)
    
    if request.method == "POST":
        survey.delete()
        return redirect("survey-list")

    return render(request, "survey/survey_confirm_delete.html", {"survey": survey})


@login_required
def edit(request, pk):
    """User can add questions to a draft survey, then activate the survey"""
    try:
        user_profile = request.user.userprofile

        survey = Survey.objects.prefetch_related("question_set__option_set").get(
            pk=pk, creator=user_profile, is_active=False
        )
    except Survey.DoesNotExist:
        raise Http404()

    if request.method == "POST":
        survey.is_active = True
        survey.save()
        return redirect("survey-detail", pk=pk)
    else:
        questions = survey.question_set.all()
        return render(request, "survey/edit.html", {"survey": survey, "questions": questions})


@login_required
def question_create(request, pk):
    """User can add a question to a draft survey"""
    try:
        user_profile = request.user.userprofile

        survey = get_object_or_404(Survey, pk=pk, creator=user_profile)
    except Survey.DoesNotExist:
        raise Http404()

    if request.method == "POST":
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.survey = survey
            question.save()
            return redirect("survey-option-create", survey_pk=pk, question_pk=question.pk)
    else:
        form = QuestionForm()

    return render(request, "survey/question.html", {"survey": survey, "form": form})


@login_required
def option_create(request, survey_pk, question_pk):
    """User can add options to a survey question"""
    try:
        user_profile = request.user.userprofile

        survey = get_object_or_404(Survey, pk=survey_pk, creator=user_profile)
        question = Question.objects.get(pk=question_pk)
    except (Survey.DoesNotExist, Question.DoesNotExist):
        raise Http404()

    if request.method == "POST":
        form = OptionForm(request.POST)
        if form.is_valid():
            option = form.save(commit=False)
            option.question_id = question_pk
            option.save()
    else:
        form = OptionForm()

    options = question.option_set.all()
    return render(
        request,
        "survey/options.html",
        {"survey": survey, "question": question, "options": options, "form": form},
    )


def start(request, pk):
    """Survey-taker can start a survey"""
    survey = get_object_or_404(Survey, pk=pk, is_active=True)
    if request.method == "POST":
        sub = Submission.objects.create(survey=survey)
        return redirect("survey-submit", survey_pk=pk, sub_pk=sub.pk)

    return render(request, "survey/start.html", {"survey": survey})


def submit(request, survey_pk, sub_pk):
    """Survey-taker submit their completed survey."""
    try:
        survey = Survey.objects.prefetch_related("question_set__option_set").get(
            pk=survey_pk, is_active=True
        )
    except Survey.DoesNotExist:
        raise Http404()

    try:
        sub = survey.submission_set.get(pk=sub_pk, is_complete=False)
    except Submission.DoesNotExist:
        raise Http404()

    questions = survey.question_set.all()
    options = [q.option_set.all() for q in questions]
    form_kwargs = {"empty_permitted": False, "options": options}
    AnswerFormSet = formset_factory(AnswerForm, extra=len(questions), formset=BaseAnswerFormSet)
    if request.method == "POST":
        formset = AnswerFormSet(request.POST, form_kwargs=form_kwargs)
        if formset.is_valid():
            with transaction.atomic():
                for form in formset:
                    Answer.objects.create(
                        option_id=form.cleaned_data["option"], submission_id=sub_pk,
                    )

                sub.is_complete = True
                sub.save()
            return redirect("survey-thanks", pk=survey_pk)

    else:
        formset = AnswerFormSet(form_kwargs=form_kwargs)

    question_forms = zip(questions, formset)
    return render(
        request,
        "survey/submit.html",
        {"survey": survey, "question_forms": question_forms, "formset": formset},
    )


def thanks(request, pk):
    """Survey-taker receives a thank-you message."""
    survey = get_object_or_404(Survey, pk=pk, is_active=True)
    return render(request, "survey/thanks.html", {"survey": survey})


