from django.urls import path

import seating_charts.views.display
import seating_charts.views.edit

app_name = 'seating_charts'

urlpatterns = [
    path('', seating_charts.views.display.index, name='seating_index'),
    path('edit/(?P<id>[0-9]+)/', seating_charts.views.edit.seatingChartEditor, name='seating_chart_editor'),
    path('edit/(?P<id>[0-9]+)/shuffle/', seating_charts.views.edit.shuffle, name='seating_chart_shuffle'),
    path('edit/(?P<id>[0-9]+)/data/', seating_charts.views.edit.seatingChartData, name='seating_chart_data'),
    path('edit/(?P<id>[0-9]+)/move/', seating_charts.views.edit.moveStudent, name='seating_chart_move'),
    path('view/(?P<id>[0-9]+)/table/', seating_charts.views.display.seatingChartByTable, name='seating_chart_view_table'),
    path('view/(?P<id>[0-9]+)/student/', seating_charts.views.display.seatingChartByStudent, name='seating_chart_view_student'),
    path('view/(?P<id>[0-9]+)/inserts.pdf', seating_charts.views.display.seatingChartInsert, name='seating_chart_view_inserts'),   
]