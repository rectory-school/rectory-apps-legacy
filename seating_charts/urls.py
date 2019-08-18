from django.urls import path

import seating_charts.views.display
import seating_charts.views.edit

app_name = 'seating_charts'

urlpatterns = [
    path('', seating_charts.views.display.index, name='seating_index'),
    path('edit/<int:id>/', seating_charts.views.edit.seatingChartEditor, name='seating_chart_editor'),
    path('edit/<int:id>/shuffle/', seating_charts.views.edit.shuffle, name='seating_chart_shuffle'),
    path('edit/<int:id>/data/', seating_charts.views.edit.seatingChartData, name='seating_chart_data'),
    path('edit/<int:id>/move/', seating_charts.views.edit.moveStudent, name='seating_chart_move'),
    path('view/<int:id>/table/', seating_charts.views.display.seatingChartByTable, name='seating_chart_view_table'),
    path('view/<int:id>/student/', seating_charts.views.display.seatingChartByStudent, name='seating_chart_view_student'),
    path('view/<int:id>/inserts.pdf', seating_charts.views.display.seatingChartInsert, name='seating_chart_view_inserts'),   
]