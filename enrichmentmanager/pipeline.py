#!/usr/bin/python

from enrichmentmanager.models import Teacher
from django.contrib.auth.models import Group

def set_groups(backend, user, response, *args, **kwargs):
    try:
        group = Group.objects.get(name="Advisors")
    except Group.DoesNotExist:
        #Bail - no advisor group
        return
        
    try:
        advisor = Teacher.objects.get(email=user.email)
        
        user.groups.add(group)
        user.save()
        
        print (user.groups)
    except Teacher.DoesNotExist:
        print("No advisor found")
