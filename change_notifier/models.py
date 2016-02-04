from django.db import models

from django.contrib.auth.models import User
from solo.models import SingletonModel

# Create your models here.
class FamilyChangeNotification(models.Model):
  users = models.ManyToManyField(User, blank=True)
  last_run = models.DateTimeField(null=True)
  
  def __str__(self):
    return "Family Change Notification Configuration"
  
  class Meta:
    verbose_name = "Family Change Notification Configuration"