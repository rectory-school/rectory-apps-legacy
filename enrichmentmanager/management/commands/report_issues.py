#!/usr/bin/python

import logging
from io import StringIO
from datetime import date

from django.core.mail import EmailMessage
from django.core.management.base import BaseCommand, CommandError

from enrichmentmanager.models import Teacher, Student, EnrichmentOption

logger = logging.getLogger("main")

class Command(BaseCommand):
    help = "Import Teachers"
    
    def add_arguments(self, parser):
        parser.add_argument('sendto', metavar='ADDRESS', nargs='+', help='The addresses the e-mail should be sent to')
    
    def handle(self, *args, **kwargs):
        logger.info("Beginning issue reporting routine")
        
        send = False
        out = StringIO()
        
        noEmailStudents = Student.objects.filter(email="")
        noEmailTeachers = Teacher.objects.filter(email="")
        
        for student in noEmailStudents:
            out.write("{name:} ({studentID:}) has no e-mail address\n".format(name=student.name, studentID=student.student_id))
            send = True
        
        for teacher in noEmailTeachers:
            adviseeCount = Student.objects.filter(advisor = teacher).count()
            enrichmentOptionCount = EnrichmentOption.objects.filter(teacher=teacher, slot__date__gte=date.today()).count()
            
            if enrichmentOptionCount or adviseeCount:
                out.write("{name:} ({teacherID:}) is relevant and has no e-mail address\n".format(name=teacher.name, teacherID=teacher.teacher_id))
                send = True
        
        
        if send:
            logger.info("Sending issue e-mail")
            message = EmailMessage("Enrichment data issues", out.getvalue(), to=kwargs['sendto'], from_email='Technology Department <technology@rectoryschool.org>')
            message.send()