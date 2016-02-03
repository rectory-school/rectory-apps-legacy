from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^$', 'seating.views.display.index', name='seating_index'),
    url(r'^edit/(?P<id>[0-9]+)/$', 'seating.views.edit.seatingChartEditor', name='seating_chart_editor'),
    url(r'^edit/(?P<id>[0-9]+)/shuffle/$', 'seating.views.edit.shuffle', name='seating_chart_shuffle'),
    url(r'^edit/(?P<id>[0-9]+)/data/$', 'seating.views.edit.seatingChartData', name='seating_chart_data'),
    url(r'^edit/(?P<id>[0-9]+)/move/$', 'seating.views.edit.moveStudent', name='seating_chart_move'),
    url(r'^view/(?P<id>[0-9]+)/table/$', 'seating.views.display.seatingChartByTable', name='seating_chart_view_table'),
    url(r'^view/(?P<id>[0-9]+)/student/$', 'seating.views.display.seatingChartByStudent', name='seating_chart_view_student'),
    url(r'^view/(?P<id>[0-9]+)/inserts.pdf$', 'seating.views.display.seatingChartInsert', name='seating_chart_view_inserts'),   
)