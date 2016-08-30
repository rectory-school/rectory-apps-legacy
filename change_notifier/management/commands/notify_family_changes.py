#!/usr/bin/python

import logging
from datetime import date

from io import StringIO

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.utils import timezone
from django.core.mail import send_mail

from academics.models import Parent, StudentParentRelation
from change_notifier.models import FamilyChangeNotification

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = "Import reset student's current status"
    
    def handle(self, *args, **kwargs):
        logger.info("Beginning family notification routine")
        
        config = FamilyChangeNotification.objects.get()
        last_run = config.last_run
        
        #If we don't have an initial date to compare to, set it to now
        if not last_run:
          config.last_run = timezone.now()
          config.save()
          
          return
        
        
        to_emails = [user.email for user in config.users.all() if user.email]
        
        if not to_emails:
          logger.error("No e-mails addresses specified")
          return 1
        
        email_body = StringIO()
        
        updated_parents = Parent.objects.filter(updated_at__gte=last_run)
        updated_parent_count = 0
        
        relevant_parents = []
        irrelevant_parents = []
        
        for parent_i, updated_parent in enumerate(updated_parents):
          if config.current_students_only:
            is_relevant = False
          
            for student_parent_relation in StudentParentRelation.objects.filter(parent=updated_parent):
              if student_parent_relation.student.current and student_parent_relation.family_id_key in ("IDFamily1", "IDFamily2"):
                is_relevant = True
                break
          else:
            #If not doing current students only, they're always relevant
            is_relevant = True
            
          if not is_relevant:
            irrelevant_parents.append(updated_parent)
            continue
          
          relevant_parents.append(updated_parent)
          
          try:
            old_version = updated_parent.history.as_of(last_run)
          except Parent.DoesNotExist as e:
            old_version = None
          
          compare_attrs = ['first_name', 'last_name', 'email', 'phone_home', 'phone_work', 'phone_cell', 'address']
          
          email_body.write("="*80 + "\n")
          email_body.write(" Family ID: {:} ".format(updated_parent.family_id).center(80, "=") + "\n")
          
          if old_version:
            email_body.write(" Existing Parent: {:} ".format(updated_parent.parent_id).center(80, "=") + "\n")
          else:
            email_body.write(" New Parent: {:} ".format(updated_parent.parent_id).center(80, "=") + "\n")
          
          
          email_body.write("="*80 + "\n\n")
          
          changed_attrs = []
          unchanged_attrs = []
          
          for attr in compare_attrs:
            if old_version:
              old_value = getattr(old_version, attr)
            else:
              old_value = ""
              
            new_value = getattr(updated_parent, attr)
            
            if old_value == new_value:
              unchanged_attrs.append((attr, old_value))
            
            else:
              changed_attrs.append((attr, old_value, new_value))
          
          email_body.write("Changed values".center(80, "-") + "\n")
          for attr, old_value, new_value in changed_attrs:
            email_body.write("{attr:}\nOld value: {old_value:}\nNew value: {new_value:}\n\n".format(attr=attr, old_value=old_value, new_value=new_value))
          
          
          email_body.write("Unchanged values".center(80, "-") + "\n")
          for i, (attr, value) in enumerate(unchanged_attrs):
            if value:
              email_body.write("{attr:}\n{value:}".format(attr=attr, value=value))
            
              if i != len(unchanged_attrs) - 1:
                email_body.write("\n\n")
          
          if parent_i != updated_parents.count() - 1:
            email_body.write("\n\n\n\n")
                    
        if relevant_parents:
          send_mail(subject="{update_count:} parent file(s) updated".format(update_count=len(relevant_parents)), message=email_body.getvalue(), from_email='technology@rectoryschool.org', recipient_list=to_emails)

        config.last_run = timezone.now()
        config.save()