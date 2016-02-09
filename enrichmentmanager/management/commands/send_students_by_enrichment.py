from datetime import date, timedelta

from django.core.management.base import BaseCommand, CommandError
from django.template.loader import get_template
from django.template import Context

from enrichmentmanager.management.commands._emailcommands import EmailCommand
from enrichmentmanager.models import EnrichmentSlot, EnrichmentOption, Student

class Command(EmailCommand):
    help = 'Sends students by enrichment report'
    
    def add_arguments(self, parser):
        super().add_arguments(parser)
        
        parser.add_argument('send_to', help='E-mail address to send report to', metavar='EMAIL', nargs="+")
    
    def handle(self, *args, **kwargs):
        self.setup(**kwargs)
        
        sendTo = map(str.strip, kwargs["send_to"])
        
        slotData = []
    
        lockouts = Student.objects.exclude(lockout="")
        
        for slot in self.slots:
            #Slot, (option, students), lockouts
            slotRow = (slot, [], lockouts)
    
            slotData.append(slotRow)
    
            q = EnrichmentOption.objects.filter(slot=slot)
        
            for option in q:
                students = option.students.filter(lockout="")
        
                slotRow[1].append((option, students))
    
    
        template = get_template('enrichmentmanager/emails/by_enrichment.html')
            
        context = Context({'slotData': slotData})
        body = template.render(context)        
        
        if self.slots.count():
            self.sendMail(
                mailFrom='Glenn Ames <games@rectoryschool.org>', 
                mailTo=sendTo,
                subject='Student Listing by Enrichment Assignments',
                bodyHTML = body
                )
