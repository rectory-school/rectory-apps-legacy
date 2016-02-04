#!/usr/bin/python

import logging
from datetime import date

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.utils import timezone

from academics.models import Parent
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
        
        updated_models = Parent.objects.filter(updated_at__gte=last_run)
        print (updated_models)