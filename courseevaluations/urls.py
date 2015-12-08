from django.conf.urls import include, url

urlpatterns = [
    url(r'^student/landing/$', 'courseevaluations.views.student_landing'),
]