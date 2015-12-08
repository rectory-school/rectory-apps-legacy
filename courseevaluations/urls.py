from django.conf.urls import include, url

urlpatterns = [
    url(r'^student/landing/$', 'courseevaluations.views.student_landing', name='courseevaluations_student_landing'),
    url(r'^student/survey/$', 'courseevaluations.views.student_survey', name='courseevaluations_student_survey'),
]