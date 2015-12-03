from django.contrib import admin

from academics.models import Dorm

class DormAdmin(admin.ModelAdmin):
    filter_horizontal = ['heads']

# Register your models here.
admin.site.register(Dorm, DormAdmin)