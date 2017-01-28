#!/usr/bin/python

import logging
from datetime import date, datetime

import time
import traceback

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.core.mail import send_mail
from django.utils import timezone

from detention_notifier.models import Detention, DetentionMailer, DetentionErrorNotification
from detention_notifier.email import get_message

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = "Send detentions"
    
    def handle(self, *args, **kwargs):
        logger.info("Beginning detention send routine")
                
        detention_mailer = DetentionMailer.objects.get()
        
        unsent_detentions = Detention.objects.filter(sent=False)
        
        if detention_mailer.do_not_send_same_day_before:
            # Convert the surpression time into a fully aware datetime object
            # so that we can compare it to the current time, and, if needed,
            # exclude detentions that were assigned today
            today = date.today()
            surpress_time = detention_mailer.do_not_send_same_day_before
            nonaware_surpress_check = datetime(today.year, today.month, today.day, surpress_time.hour, surpress_time.minute)
            surpress_check = timezone.get_current_timezone().localize(nonaware_surpress_check)
            
            # It has not yet hit the time required to send today's detentions
            if timezone.now() < surpress_check:
                # Only include detentions *before* today
                unsent_detentions = unsent_detentions.filter(detention_date__lt=date.today())
        
        error_recipients = [o.address for o in DetentionErrorNotification.objects.filter(mailer=detention_mailer)]
        
        for detention in unsent_detentions:
            try:
                message = get_message(detention)
                message.send()
                
                #Sleep for 1 second for SES rate limiting
                #time.sleep(1)
                
                detention.sent = True
                detention.save()
                
            except ValueError as e:
                send_mail("Error sending detention", str(e), 'technology@rectoryschool.org', error_recipients)
                continue

            except Exception as e:
                full_exception = traceback.format_exc()
                send_mail("Detention mailer internal error", full_exception, 'technology@rectoryschool.org', error_recipients)
                continue
