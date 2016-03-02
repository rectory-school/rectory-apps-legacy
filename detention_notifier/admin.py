from django.contrib import admin
from django.core.mail import send_mail

from solo.admin import SingletonModelAdmin
from detention_notifier.models import DetentionMailer, Offense, Detention, Code, DetentionCC, DetentionTo, DetentionErrorNotification
from detention_notifier.email import get_message

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
    list_display = ['__str__', 'sent', 'offense', 'detention_date', 'student', 'teacher']
    
    list_filter = ['code', 'term', 'sent']
    
    search_fields = ['id', 'student__first_name', 'student__last_name']
    
    ordering = ['-detention_date']
    actions = ['send_to_me']
    
    def send_to_me(self, request, queryset):
        if not request.user.email:
            raise ValueError("No e-mail address for {} when trying to send a sample detention e-mail.".format(request.user))
        
        for detention in queryset:
            try:
                message = get_message(detention, override_recipients=[request.user.email])
            except ValueError as e:
                send_mail("Error sending detention", str(e), 'technology@rectoryschool.org', [request.user.email])
                continue
                
            message.send()
    
    send_to_me.short_description = "Send me a sample of this detention report"
    
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