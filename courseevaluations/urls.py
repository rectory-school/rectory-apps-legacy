from django.conf.urls import include, url

urlpatterns = [
    url(r'^student/landing/$', 'courseevaluations.views.student.student_landing', name='courseevaluations_student_landing'),
    url(r'^student/survey/$', 'courseevaluations.views.student.student_survey', name='courseevaluations_student_survey'),

    url(r'^reports/(?P<id>[0-9]+)/$', 'courseevaluations.views.reports.index', name='courseevaluations_reports_index'),
    url(r'^reports/(?P<id>[0-9]+)/summary_by_student/$', 'courseevaluations.views.reports.by_student', name='courseevaluations_reports_by_student', kwargs={'show_evaluables': False}),
    url(r'^reports/(?P<id>[0-9]+)/detail_by_student/$', 'courseevaluations.views.reports.by_student', name='courseevaluations_reports_by_student', kwargs={'show_evaluables': True}),
]