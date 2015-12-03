from django.contrib import admin

from academics.models import Dorm, AcademicYear

class DormAdmin(admin.ModelAdmin):
    filter_horizontal = ['heads']

class AcademicYearAdmin(admin.ModelAdmin):
    fields = ['year', 'current']
    list_display = ['year', 'current']
    readonly_fields = ['year']

# Register your models here.
admin.site.register(Dorm, DormAdmin)
admin.site.register(AcademicYear, AcademicYearAdmin)