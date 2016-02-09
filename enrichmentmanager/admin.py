from django.contrib import admin
from enrichmentmanager.models import Teacher, Student, EnrichmentOption, EnrichmentSlot, EnrichmentSignup, EmailSuppression
from simple_history.admin import SimpleHistoryAdmin

class EnrichmentOptionInline(admin.TabularInline):
    model = EnrichmentOption

class EnrichmentSlotAdmin(admin.ModelAdmin):
    inlines = [EnrichmentOptionInline]
    
class StudentAdmin(admin.ModelAdmin):
    fields = ["academic_student", "advisor", "lockout"]
    search_fields = ["academic_student__first_name", "academic_student__last_name"]
    
    readonly_fields = ("academic_student", "advisor")
    
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