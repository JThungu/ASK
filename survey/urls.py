from .views import create_profile, export_results_csv
from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from . import views
from .views.survey import create_profile
from .views.survey import export_results_csv

urlpatterns = [
    path("", views.landing, name="landing"),
    path("accounts/", include('allauth.urls')),
    path("surveys/", views.survey.survey_list, name="survey-list"),
    path("surveys/<int:pk>/", views.survey.detail, name="survey-detail"),
    path("surveys/create/", views.survey.create, name="survey-create"),
    path("surveys/<int:pk>/delete/", views.survey.delete, name="survey-delete"),
    path("surveys/<int:pk>/edit/", views.survey.edit, name="survey-edit"),
    path("surveys/<int:pk>/question/", views.survey.question_create, name="survey-question-create"),
    path(
        "surveys/<int:survey_pk>/question/<int:question_pk>/option/",
        views.survey.option_create,
        name="survey-option-create",
    ),
    path("surveys/<int:pk>/start/", views.survey.start, name="survey-start"),
    path("surveys/<int:survey_pk>/submit/<int:sub_pk>/", views.survey.submit, name="survey-submit"),
    path("surveys/<int:pk>/thanks/", views.survey.thanks, name="survey-thanks"),
    path("create-profile/", views.create_profile, name="create-profile"),
    path("surveys/<int:pk>/export-csv/", views.export_results_csv, name="survey-export-csv"),  # Add this line for export view
    path("admin/", admin.site.urls),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [path("__debug__/", include(debug_toolbar.urls))]

