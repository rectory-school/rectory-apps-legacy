from django.contrib import admin

from solo.admin import SingletonModelAdmin
from change_notifier.models import FamilyChangeNotification

class FamilyChangeNotificationAdmin(SingletonModelAdmin):
  fields = ['users']
  filter_horizontal = ['users']
  
admin.site.register(FamilyChangeNotification, FamilyChangeNotificationAdmin)