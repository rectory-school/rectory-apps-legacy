#!/usr/bin/python

import logging
from datetime import date

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.core.urlresolvers import reverse
from django.core.mail import send_mail, EmailMessage

from academics.models import Student, Teacher
from courseevaluations.models import EvaluationSet, Evaluable
from academics.utils import fmpxmlparser

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = "Import IIP Evaluations"
    
    def add_arguments(self, parser):
        parser.add_argument('--override_to', metavar='EMAILOVERRIDE', help='The address to override an outgoing email to')
        parser.add_argument('--one_random',action='store_const', const=True, default=False, help='The address to override an outgoing email to')
        
    def handle(self, *args, **kwargs):
        logger.info("Beginning IIP import routine")
        
        evaluation_sets = EvaluationSet.objects.open()
        evaluables = Evaluable.objects.filter(evaluation_set__in=evaluation_sets, complete=False)
        students = Student.objects.filter(evaluable__in=evaluables).distinct()
        
        if kwargs["one_random"]:
            students = [students.order_by("?").first()]
        
        for student in students:
            url = "http://apps.rectoryschool.org{url:}?auth_key={auth_key:}".format(url=reverse('courseevaluations_student_landing'), auth_key=student.auth_key)
            
            message = TEMPLATE.format(first=student.first_name, last=student.last_name, link=url)
            
            if kwargs["override_to"]:
                mail_to = [kwargs["override_to"]]
            else:
                mail_to = [student.email]
            
            msg = EmailMessage("Course Evaluations", message, "Mrs. Hart <lhart@rectoryschool.org>", ["adam@thepeacock.net"])
            msg.content_subtype = "html"
            msg.send()
        

TEMPLATE = """<p>To {first:},</p>
 
<p>Teachers continue to strive to learn and to grow.  The December, we are asking all students to complete an evaluation for all courses and for boarding students, a dorm evaluation.  The answers will be collected online, and faculty will not see your name associated with individual responses.</p>
 
<p>There is an on-line evaluation for each course and dorm. <br />
<a href="{link:}">Click here for your dorm evaluations</a></p>
 
<p>The link will take you to your Course/Dorm Evaluation page.  Please select one evaluation, complete the evaluation and click “Record My Answers.”  Please work your way through each evaluation until all course/dorm evaluations have been moved to your completed list.</p>
 
<p>Thank you for giving us your feedback as soon as possible.</p>
  
<p>Mrs. Hart <br />
Director of Innovation</p>
 
<p>If the above link does not work for you, please copy/paste the following URL into your browser:<br />{link:}</p>"""