from datetime import date

from django.core.management.base import BaseCommand, CommandError
from django.template.loader import get_template
from django.template import Context
from django.conf import settings

from enrichmentmanager.management.commands._emailcommands import EmailCommand
from enrichmentmanager.lib import getUnassignedStudents, getUnassignedAdvisors

class Command(EmailCommand):
    help = 'Sends an e-mail to all the advisors with missing students'
    
    def add_arguments(self, parser):
        super().add_arguments(parser)
        
        parser.add_argument('send_to', help='E-mail address to send report to', metavar='EMAIL', nargs="+")
                    
            
    def handle(self, *args, **kwargs):
        self.setup(**kwargs)
        
        sendTo = map(str.strip, kwargs["send_to"])
        
        #Format: bySlot[slot][advisor]['students'] = [students]
        bySlot = {}
        allStudents = set()
        
        for slot in self.slots:
            if not slot in bySlot:
                bySlot[slot] = {}
                
            missingStudents = getUnassignedStudents([slot])
            
            for student in sorted(missingStudents, key=lambda s: (s.last_name, s.first_name, s.nickname)):
                advisor = student.advisor
                allStudents.add(student)
                
                if not advisor in bySlot[slot]:
                    bySlot[slot][advisor] = {'students': []}
                
                bySlot[slot][advisor]['students'].append(student)
        
        #(slot, [(advisor, [students])])
        flattenedData = []
        for slot in bySlot:
            out = []
            
            for advisor in sorted(bySlot[slot], key=lambda a: (a.last_name, a.first_name)):
                out.append((advisor, bySlot[slot][advisor]['students']))
            
            flattenedData.append((slot, out))
        
        template = get_template('enrichmentmanager/emails/unassigned_administrator.html')
        count = len(allStudents)
        
        context = Context({'slots': flattenedData, 'count': count, 'base_url': settings.MAIL_BASE_URL})
        body = template.render(context)
        
        if self.slots.count():
            self.sendMail(
                mailFrom='Technology <technology@rectoryschool.org>', 
                mailTo=sendTo,
                subject='Master List of Unassigned Advisees for Enrichment',
                replyTo=['lhart@rectoryschool.org', 'games@rectoryschool.org', 'justin.bendall@rectoryschool.org', 'adam.peacock@rectoryschool.org'],
                bodyHTML = body
                )