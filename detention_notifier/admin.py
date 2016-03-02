from django.contrib import admin

from solo.admin import SingletonModelAdmin
from detention_notifier.models import DetentionMailer, Offense, Detention, Code, DetentionCC, DetentionTo, DetentionErrorNotification

class DetentionToInline(admin.TabularInline):
    model = DetentionTo

class DetentionCCInline(admin.TabularInline):
    model = DetentionCC

class DetentionErrorInline(admin.TabularInline):
    model = DetentionErrorNotification

class DetentionMailerAdmin(SingletonModelAdmin):
    inlines = [DetentionToInline, DetentionCCInline, DetentionErrorInline]

class CodeAdmin(admin.ModelAdmin):
    fields = ['code', 'process']
    readonly_fields = ['code']
    
    list_display = ['code', 'process']
    
class DetentionAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'sent', 'offense', 'student', 'teacher']
    
    list_filter = ['code', 'term', 'sent']
    
    search_fields = ['id', 'student__first_name', 'student__last_name']
    
class OffenseAdmin(admin.ModelAdmin):
    fields = ['offense', 'sentence_insert', 'mail', 'email_listing', 'sentence_example']
    readonly_fields = ['sentence_example']
    
    def sentence_example(self, obj):
        if obj.sentence_insert:
            return "Adam Peacock got a detention from Glenn Ames {}.".format(obj.sentence_insert)
        
        return None
    
    sentence_example.short_description = "Example sentence"
    sentence_example.empty_value_display = "N/A"

admin.site.register(DetentionMailer, DetentionMailerAdmin)
admin.site.register(Offense, OffenseAdmin)
admin.site.register(Detention, DetentionAdmin)
admin.site.register(Code, CodeAdmin)