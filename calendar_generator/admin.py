from django.contrib import admin

from calendar_generator.models import Calendar, Day, SkipDate, ResetDate
from adminsortable.admin import NonSortableParentAdmin, SortableStackedInline

class DayInline(SortableStackedInline):
    model = Day
    extra = 0

class SkipDateInline(admin.StackedInline):
    model = SkipDate
    extra = 0

class ResetDateInline(admin.StackedInline):
    model = ResetDate
    extra = 0

class CalendarAdmin(NonSortableParentAdmin):
    inlines = [DayInline, SkipDateInline, ResetDateInline]
    
    change_form_template_extends = "admin/calendar_generator/calendar/change_form.html"

admin.site.register(Calendar, CalendarAdmin)