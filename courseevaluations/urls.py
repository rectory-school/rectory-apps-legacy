from django.conf.urls import include, url

urlpatterns = [
    url(r'^student/landing/$', 'courseevaluations.views.student.student_landing', name='courseevaluations_student_landing'),
    url(r'^student/survey/$', 'courseevaluations.views.student.student_survey', name='courseevaluations_student_survey'),

    url(r'^reports/$', 'courseevaluations.views.reports.index', name='courseevaluations_reports_status_index'),
    url(r'^reports/(?P<id>[0-9]+)/$', 'courseevaluations.views.reports.evaluation_set_index', name='courseevaluations_reports_status_index'),
    url(r'^reports/(?P<id>[0-9]+)/summary_by_student/$', 'courseevaluations.views.reports.by_student', name='courseevaluations_reports_by_student', kwargs={'show_evaluables': False}),
    url(r'^reports/(?P<id>[0-9]+)/detail_by_student/$', 'courseevaluations.views.reports.by_student', name='courseevaluations_reports_by_student', kwargs={'show_evaluables': True}),
    
    url(r'^reports/(?P<id>[0-9]+)/by_section/$', 'courseevaluations.views.reports.by_section', name='courseevaluations_reports_by_section'),
    
    url(r'^email/send/student/$', 'courseevaluations.views.reports.send_student_email', name='courseevaluations_send_student_email'),
    url(r'^email/send/advisor_tutor_status/$', 'courseevaluations.views.reports.send_advisor_tutor_status', name='courseevaluations_send_advisor_tutor_status'),
    url(r'^email/send/section_status/$', 'courseevaluations.views.reports.send_teacher_per_section_email', name='courseevaluatons_send_teacher_per_section_email'),
]