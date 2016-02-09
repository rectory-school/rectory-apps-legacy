import logging
from datetime import date, timedelta

from django.core.management.base import BaseCommand, CommandError
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.conf import settings

from premailer import transform

from enrichmentmanager.models import EnrichmentSlot, EmailSuppression

log = logging.getLogger(__name__)

class EmailCommand(BaseCommand):
    help = 'Sends an e-mail to all the advisors with missing students'
    
    def setup(self, **kwargs):
        workingDate = kwargs['base_date']
        
        if type(workingDate) == str:
            y, m, d = map(int, workingDate.split("-"))
            self.baseDate = date(y, m, d)
            
        elif type(workingDate) == date:
            self.baseDate = workingDate
        
        else:
            TypeError("Date is of type {type:}".format(type=type(workingDate)))
        
        self.startDate = self.baseDate + timedelta(kwargs['start_days_ahead'])
        self.endDate = self.baseDate + timedelta(kwargs['end_days_ahead'])
        
        if self.startDate > self.endDate:
            raise ValueError("Start date is after end date")
        
        self.slots = EnrichmentSlot.objects.filter(date__gte=self.startDate, date__lte=self.endDate)
        
        if kwargs['override_email']:
            self.overrideEmail = [kwargs['override_email']]
        else:
            self.overrideEmail = None
    
    def sendMail(self, mailFrom='technology@rectoryschool.org', mailTo=None, mailCC=None, mailBCC=None, replyTo=None, subject=None, bodyHTML=None, bodyText=None):
        surpress = (EmailSuppression.objects.filter(suppression_date=date.today()).count() > 0)
        
        if surpress:
            log.warn("Surpressing e-mail")
            return
            
        if bodyText and bodyHTML:
            message = EmailMultiAlternatives()
            message.body = bodyText
            message.attach_alternative(transform(bodyHTML), "text/html")
            
        elif bodyText:
            message = EmailMessage()
            message.body = bodyText
            
        elif bodyHTML:
            message = EmailMessage()
            message.body = transform(bodyHTML)
            message.content_subtype = "html"
        else:
            raise TypeError("bodyHTML or bodyText must be set")
        
        if not (mailTo or mailCC or mailBCC):
            raise TypeError("Message must have at least one recipient")
        
        if subject:
            message.subject = subject
        
        
        overrideEmail = None
        
        #Try to get override email from settings
        try:
             overrideEmail = [settings.ENRICHMENT_OVERRIDE_EMAIL]
        except AttributeError:
            pass
        
        #Take presidence on the parameter
        if self.overrideEmail:
            overrideEmail = self.overrideEmail
        
        if not overrideEmail:
            if mailTo:
                message.to = list(mailTo)
    
            if mailCC:
                message.cc = list(mailCC)
    
            if mailBCC:
                message.bcc = list(mailBCC)
        else:
            message.to = overrideEmail
        
        if replyTo:
            message.reply_to = list(replyTo)
        
                
        message.from_email = mailFrom
        message.send()
        
    def add_arguments(self, parser):
        parser.add_argument('--override_email', 
            help='Force all e-mails to go to EMAIL', metavar='EMAIL')
        
        parser.add_argument('--base_date',
            help='Base date for slot finding', metavar='EMAIL', default=date.today())
        
        parser.add_argument('--start_days_ahead',
            help='Start finding slots base date + days', default=0, type=int)
        
        parser.add_argument('--end_days_ahead',
            help='Stop finding slots base date + days', default=0, type=int)
            
        parser.add_argument('--editable_only',
            help='Only find slots that are currently editable', action='store_const', const=True, default=False)
