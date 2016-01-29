from django.conf.urls import include, url

urlpatterns = [
    url(r'^text/(?P<id>[0-9]+)/$', 'calendar_generator.views.calendar_days_text', name='calendar_generator_days_text'),
]