from django.conf.urls import url

import calendar_generator.views

app_name = 'calendar_generator'

urlpatterns = [
    url(r'^text/(?P<id>[0-9]+)/$', calendar_generator.views.calendar_days_text, name='calendar_generator_days_text'),
    url(r'^pdf/month-by-month/(?P<id>[0-9]+)/$', calendar_generator.views.full_calendar_pdf, name='calendar_generator_days_pdf'),
    url(r'^pdf/one-page/(?P<id>[0-9]+)/$', calendar_generator.views.one_page_calendar, name='calendar_generator_one_page_pdf'),
    url(r'^pdf/custom/(?P<id>[0-9]+)/$', calendar_generator.views.custom_pdf, name='calendar_generator_custom_pdf'),
    
    url(r'^zip/(?P<id>[0-9]+)/$', calendar_generator.views.full_zip, name='calendar_generator_days_zip'),
]