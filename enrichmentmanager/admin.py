from django.contrib import admin
from enrichmentmanager.models import Teacher, Student, EnrichmentOption, EnrichmentSlot, EnrichmentSignup, EmailSuppression
from simple_history.admin import SimpleHistoryAdmin

class EnrichmentOptionInline(admin.TabularInline):
    model = EnrichmentOption

class EnrichmentSlotAdmin(admin.ModelAdmin):
    inlines = [EnrichmentOptionInline]
    
class StudentAdmin(admin.ModelAdmin):
    fields = ["first_name", "last_name", "lockout"]
    search_fields = ["first_name", "last_name"]
    
    readonly_fields = ("first_name", "last_name")

class EnrichmentSignupAdmin(admin.ModelAdmin):
    list_filter = ['slot', 'student']

# Register your models here.
admin.site.register(Teacher)
admin.site.register(Student, StudentAdmin)
admin.site.register(EnrichmentSlot, EnrichmentSlotAdmin)
#admin.site.register(EnrichmentOption, EnrichmentOptionAdmin)
admin.site.register(EnrichmentSignup, EnrichmentSignupAdmin)
admin.site.register(EmailSuppression)