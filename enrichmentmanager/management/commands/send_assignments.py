import logging
from datetime import date, timedelta

from django.core.management.base import BaseCommand, CommandError
from django.template.loader import get_template
from django.template import Context

from enrichmentmanager.management.commands._emailcommands import EmailCommand
from enrichmentmanager.lib import getUnassignedStudents, getUnassignedAdvisors
from enrichmentmanager.models import EnrichmentOption, Student, Teacher, EnrichmentSlot, EnrichmentSignup

from io import StringIO

class Command(EmailCommand):
    help = 'Sends an e-mail with student locations to advisors, students and teachers with their relevant locations'
    
    def add_arguments(self, parser):
        super().add_arguments(parser)

    def handle(self, *args, **kwargs):
        self.setup(**kwargs)
        
        for slot in self.slots:
            unassigned = set()
            
            #Students
            for student in Student.objects.exclude(email=""):
                if not student.email:
                    logger.error("Student {} ({}) has no e-mail address to send the assignment report to".format(student.student_id, student.id))
                    continue
                
                try:
                    signup = EnrichmentSignup.objects.get(student=student, slot=slot)
                    option = signup.enrichment_option
                    message = "Dear {name:},\n\nYour assigned enrichment session on {date:} is in {room:} with {teacher:}.".format(name=student.name, date=slot.date.strftime("%A, %B %d"), room=option.location, teacher=option.teacher)
                except EnrichmentSignup.DoesNotExist:
                    message = "Dear {name:},\n\nYou were not assigned an enrichment session on {date:}. Please report to the education office during enrichment.".format(date=slot.date.strftime("%A, %B %d"), name=student.name)
                    unassigned.add(student)

                self.sendMail(
                    mailFrom='Technology Department <technology@rectoryschool.org>', 
                    mailTo=[student.email],
                    mailBCC=['adam.peacock@rectoryschool.org'],
                    replyTo=[student.advisor.email],
                    subject="Enrichment assignment for {date:}".format(date=slot.date.strftime("%A, %B %d")),
                    bodyText = message
                    )
                
            #Advisors
            for advisor in Teacher.objects.exclude(student=None):
                if not advisor.email:
                    logger.error("Teacher {} ({}) has no e-mail address to send the advisor assignment report to".format(advisor.teacher_id, advisor.id))
                    continue
            
                out = StringIO()
            
                out.write("Dear {name:},\n\nYour advisee's assignments for {date:} are as follows:\n".format(name=advisor.name, date=slot.date.strftime("%A, %B %d, %Y")))
            
                for student in advisor.student_set.all():
                    try:
                        signup = EnrichmentSignup.objects.get(student=student, slot=slot)
                        option = signup.enrichment_option
                    
                        out.write("{student:}: {room:} with {teacher:}\n".format(student=student.name, room=option.location, teacher=option.teacher.name))
                    
                    except EnrichmentSignup.DoesNotExist:
                        out.write("{student:}: Unassigned. Please contact the education office.\n".format(student=student.name))
                
                self.sendMail(
                    mailFrom='Technology Department <technology@rectoryschool.org>', 
                    mailTo=[advisor.email],
                    mailBCC=['adam.peacock@rectoryschool.org'],
                    replyTo=['games@rectoryschool.org'],
                    subject="Advisee enrichment assignments for {date:}".format(date=slot.date.strftime("%A, %B %d")),
                    bodyText = out.getvalue()
                    )
                            
            #Teachers
            for option in EnrichmentOption.objects.filter(slot=slot):
                if not option.teacher.email:
                    logger.error("Teacher {} ({}) has no e-mail address to send the enrichment option assignment report to".format(option.teacher.teacher_id, option.teacher.id))
                    continue

                out = StringIO()
            
                count = option.students.count()
            
                if count > 0:
                    out.write("Dear {name:},\n\n".format(name=option.teacher.name))
                
                    if count == 1:
                        out.write("You have one student coming to see you on {date:} during enrichment.\n\n".format(date=slot.date.strftime("%A, %B %d")))
                    else:
                        out.write("You have {count:} students coming to see you on {date:} during enrichment.\n\n".format(date=slot.date.strftime("%A, %B %d"), count=count))
                
                    out.write("Location: {location:}\n\n".format(location=option.location))
                
                    out.write("Student list:\n")
                
                    for student in option.students.all():
                        out.write("{name:}\n".format(name=student.name))

                else:
                    out.write("Dear {name:},\n\nNo students are signed up for your enrichment session on {date:}.\n\nPlease stay in your assigned location as you may still get a student coming for extra help.\n\nLocation: {room:}".format(name=option.teacher.name, date=slot.date.strftime("%A, %B %d"), room=option.location))
            
            
                self.sendMail(
                    mailFrom='Technology Department <technology@rectoryschool.org>', 
                    mailTo=[option.teacher.email],
                    mailBCC=['adam.peacock@rectoryschool.org'],
                    replyTo=['games@rectoryschool.org'],
                    subject="Students coming for enrichment on {date:}".format(date=slot.date.strftime("%A, %B %d")),
                    bodyText = out.getvalue()
                    )
