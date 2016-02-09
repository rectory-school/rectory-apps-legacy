from django.conf.urls import include, url
from django.contrib import admin

import enrichmentmanager.views.assign as views_assign
import enrichmentmanager.views.reporting as views_reporting

urlpatterns = [
    url(r'^$', views_assign.index, name="enrichment_index"),
    
    url(r'^assign/save/$', views_assign.save_assignments, name='save_assignments'),
    
    url(r'^assign/$', views_assign.advisor_quick, name='assign_advisor'),
    url(r'^assign/(?P<advisor>[0-9]+)/(?P<year>[0-9]{4})-(?P<month>[0-9]{1,2})-(?P<day>[0-9]{1,2})/$', views_assign.advisor_explicit, name='assign_advisor'),
    
    url(r'^assign/student/(?P<student_id>[0-9]+)/$', views_assign.single_student, name='assign_single_student'),
    url(r'^assign/student/(?P<student_id>[0-9]+)/(?P<weekday>[0|1|2|3|4|5|6])/$', views_assign.single_student, name='assign_single_student'),
    
    url(r'^assign/all/$', views_assign.all_quick, name='assign_all'),
    url(r'^assign/all/(?P<year>[0-9]{4})-(?P<month>[0-9]{1,2})-(?P<day>[0-9]{1,2})/$', views_assign.all_explicit, name='assign_all'),
    
    url(r'^assign/unassigned/$', views_assign.unassigned_quick, name='assign_unassigned'),
    url(r'^assign/unassigned/(?P<year>[0-9]{4})-(?P<month>[0-9]{1,2})-(?P<day>[0-9]{1,2})/$', views_assign.unassigned_explicit, name='assign_unassigned'),
    
    url(r'^reports/$', views_reporting.index, name='reporting_index'),
    url(r'^reports/unassigned/(?P<year>[0-9]{4})-(?P<month>[0-9]{1,2})-(?P<day>[0-9]{1,2})/$', views_reporting.grid, name='reporting_unassigned', kwargs={'unassigned': True}),
    url(r'^reports/locations/(?P<year>[0-9]{4})-(?P<month>[0-9]{1,2})-(?P<day>[0-9]{1,2})/$', views_reporting.room_counts, name='reporting_locations'),
    url(r'^reports/assigned/(?P<year>[0-9]{4})-(?P<month>[0-9]{1,2})-(?P<day>[0-9]{1,2})/$', views_reporting.grid, name='reporting_assigned', kwargs={'unassigned': False}),
    url(r'^reports/for_teacher/(?P<teacher>[0-9]+)/(?P<year>[0-9]{4})-(?P<month>[0-9]{1,2})-(?P<day>[0-9]{1,2})/$', views_reporting.by_enrichment_option, name='reporting_by_enrichment_option', kwargs={'dateOnly': True}),
    url(r'^reports/by_option/(?P<year>[0-9]{4})-(?P<month>[0-9]{1,2})-(?P<day>[0-9]{1,2})/$', views_reporting.by_enrichment_option, name='reporting_by_enrichment_option'),
    url(r'^reports/by_student/(?P<year>[0-9]{4})-(?P<month>[0-9]{1,2})-(?P<day>[0-9]{1,2})/$', views_reporting.by_student, name='reporting_by_student'),
    url(r'^reports/printable_student/(?P<advisor>[0-9]+)/(?P<year>[0-9]{4})-(?P<month>[0-9]{1,2})-(?P<day>[0-9]{1,2})/$', views_reporting.student_printable, name='reporting_student_printable'),
    url(r'^reports/printable_student/(?P<year>[0-9]{4})-(?P<month>[0-9]{1,2})-(?P<day>[0-9]{1,2})/$', views_reporting.student_printable, name='reporting_student_printable'),
    url(r'^email_demo/$', views_reporting.email_demo),
]
