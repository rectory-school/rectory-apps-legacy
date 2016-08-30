from django.contrib import admin

from adminsortable.admin import SortableAdmin

from seating_charts.models import Table, MealTime, SeatFiller, PinnedStudent, Layout, SeatingStudent, Ethnicity

class SeatFillerInline(admin.TabularInline):
	model = SeatFiller
	extra = 0

class PinnedStudentInline(admin.TabularInline):
	model = PinnedStudent
	extra = 0
	
class TableAdmin(admin.ModelAdmin):
    filter_horizontal = ['for_meals']
    inlines = [SeatFillerInline, PinnedStudentInline]

class MealTimeAdmin(SortableAdmin):
    filter_horizontal = ['include_grades']

class SeatingStudentAdmin(admin.ModelAdmin):
  fields = ['enrollment', 'ethnicity', 'food_allergy']
  readonly_fields = ['enrollment']
  
  list_filter = ['enrollment__grade', 'enrollment__grade__school', 'ethnicity']
  list_display = ['__str__', 'ethnicity', 'food_allergy']
  list_editable = ['ethnicity', 'food_allergy']
  
  def has_add_permission(request, *args, **kwargs):
    return False
  
  def has_delete_permission(request, obj=None, *args, **kwargs):
    return False
  
  
admin.site.register(Table, TableAdmin)
admin.site.register(MealTime, MealTimeAdmin)
admin.site.register(Layout)
admin.site.register(SeatingStudent, SeatingStudentAdmin)
admin.site.register(Ethnicity)