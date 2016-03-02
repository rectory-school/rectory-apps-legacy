from datetime import date, datetime, time, timedelta

from django.contrib import admin
from django.utils import timezone

from enrichmentmanager.models import Teacher, Student, EnrichmentOption, EnrichmentSlot, EnrichmentSignup, EmailSuppression
from simple_history.admin import SimpleHistoryAdmin

class EditableUntilListFilter(admin.SimpleListFilter):
    title = 'edit cutoff'
    
    parameter_name = 'editable_until'
    
    def lookups(self, request, model_admin):
        return (
            ('empty', 'No edit cutoff'),
        )
    
    def queryset(self, request, queryset):
        if self.value() == 'empty':
            return queryset.filter(editable_until=None)

class SlotDateFilter(admin.SimpleListFilter):
    title = 'slot date'
    
    parameter_name = 'slot_date'
    
    def lookups(self, request, model_admin):
        return (
            ('future', 'After today'),
            ('past', 'Before today'),
            ('today', 'Today'),
        )
    
    def queryset(self, request, queryset):
        if self.value() == 'future':
            return queryset.filter(date__gt = date.today())
        
        if self.value() == 'past':
            return queryset.filter(date__lt = date.today())
        
        if self.value() == 'today':
            return queryset.filter(date = date.today())
            
class EnrichmentOptionInline(admin.TabularInline):
    model = EnrichmentOption

class EnrichmentSlotAdmin(admin.ModelAdmin):
    inlines = [EnrichmentOptionInline]
    
    list_display = ['date', 'editable_until']
    
    actions = ['allow_edit_until_1_10_0', 'allow_edit_until_1_12_0', 'allow_edit_until_1_14_0', 'allow_edit_until_1_17_0']
    
    list_filter = (EditableUntilListFilter, SlotDateFilter, )
    
    def reset_edit_time(self, queryset, days_before, time_hours_before, time_minutes_before):
        for slot in queryset:
            editable_date = slot.date - timedelta(days=days_before)
            editable_until_notz = datetime(
                                        editable_date.year, 
                                        editable_date.month, 
                                        editable_date.day,
                                        time_hours_before,
                                        time_minutes_before,
                                        0)
            
            editable_until = timezone.get_current_timezone().localize(editable_until_notz)
            
            slot.editable_until = editable_until
            slot.save()

    def allow_edit_until_1_10_0(self, request, queryset):
        self.reset_edit_time(queryset, 1, 10, 0)

    def allow_edit_until_1_12_0(self, request, queryset):
        self.reset_edit_time(queryset, 1, 12, 0)
    
    def allow_edit_until_1_14_0(self, request, queryset):
        self.reset_edit_time(queryset, 1, 14, 0)
        
    def allow_edit_until_1_17_0(self, request, queryset):
        self.reset_edit_time(queryset, 1, 17, 0)
    
    allow_edit_until_1_10_0.short_description = "Allow editing until 10 AM on the day before"
    allow_edit_until_1_12_0.short_description = "Allow editing until noon on the day before"    
    allow_edit_until_1_14_0.short_description = "Allow editing until 2 PM on the day before"
    allow_edit_until_1_17_0.short_description = "Allow editing until 5 PM on the day before"
    
class StudentAdmin(admin.ModelAdmin):
    fields = ["academic_student", "advisor", "lockout", "associated_teachers"]
    search_fields = ["academic_student__first_name", "academic_student__last_name"]
    
    readonly_fields = ("academic_student", "advisor", "associated_teachers")
    
    search_fields = ["academic_student__first_name", "academic_student__last_name"]
    
    def has_add_permission(self, *args, **kwargs):
        return False
    
    def has_delete_permission(self, *args, **kwargs):
        return False

class TeacherAdmin(admin.ModelAdmin):
    fields = ["academic_teacher", 'default_room', 'default_description']
    readonly_fields = ["academic_teacher", 'default_room', 'default_description']
    list_filter = ['academic_teacher__active']
    
    def has_add_permission(self, *args, **kwargs):
        return False
    
    def has_delete_permission(self, *args, **kwargs):
        return False

class EnrichmentSignupAdmin(admin.ModelAdmin):
    list_filter = ['slot', 'student']

# Register your models here.
admin.site.register(Teacher, TeacherAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(EnrichmentSlot, EnrichmentSlotAdmin)
admin.site.register(EnrichmentSignup, EnrichmentSignupAdmin)
admin.site.register(EmailSuppression)