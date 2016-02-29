from django.contrib import admin

from solo.admin import SingletonModelAdmin
from detention_notifier.models import DetentionMailer

class DetentionMailerAdmin(SingletonModelAdmin):
    pass
#  fields = ['users']
#  filter_horizontal = ['users']

  
admin.site.register(DetentionMailer, DetentionMailerAdmin)