import logging
from datetime import date, timedelta

from django.core.management.base import BaseCommand, CommandError
from django.template.loader import get_template
from django.template import Context

from enrichmentmanager.management.commands._emailcommands import EmailCommand
from enrichmentmanager.lib import getUnassignedStudents, getUnassignedAdvisors

logger = logging.getLogger("main")

class Command(EmailCommand):
    help = 'Sends an e-mail to all the advisors with missing students'
    
    def add_arguments(self, parser):
        super().add_arguments(parser)
    
    def handle(self, *args, **kwargs):
        self.setup(**kwargs)
        
        #Format: byAdvisor[advisor][slot]
        byAdvisor = {}
        
        for slot in self.slots:
            missingStudents = getUnassignedStudents([slot])
            
            for student in sorted(missingStudents, key=lambda s: (s.last_name, s.first_name, s.nickname)):
                advisor = student.advisor
                
                if not advisor in byAdvisor:
                    byAdvisor[advisor] = {}
                
                if not slot in byAdvisor[advisor]:
                    byAdvisor[advisor][slot] = {'students': []}
                
                byAdvisor[advisor][slot]['students'].append(student)
            
        
        for advisor in byAdvisor:
            allStudents = set()
            
            flattenedSlots = []
            for slot in sorted(byAdvisor[advisor].keys(), key=lambda s: s.date):
                students = byAdvisor[advisor][slot]['students']
                allStudents |= set(students)
                flattenedSlots.append((slot, students))
            
            studentCount = len(allStudents)
            
            if studentCount:
                deadline = min([slot.editable_until for slot in byAdvisor[advisor].keys() if slot.editable_until]) - timedelta(hours=1)
                
                template = get_template('enrichmentmanager/emails/unassigned_advisor.html')
                context = Context({'slots': flattenedSlots, 'count': studentCount, 'advisor': advisor, 'deadline': deadline, 'base_url': settings.MAIL_BASE_URL})
                body = template.render(context)
            
                self.sendMail(
                    mailFrom='Glenn Ames <games@rectoryschool.org>', 
                    mailTo=[advisor.email],
                    mailCC=['adam.peacock@rectoryschool.org', 'lhart@rectoryschool.org'], 
                    replyTo=['adam.peacock@rectoryschool.org', 'lhart@rectoryschool.org', 'games@rectoryschool.org'],
                    subject='Unassigned Advisees for Enrichment',
                    bodyHTML = body
                    )
