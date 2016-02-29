#!/usr/bin/python

import logging
from datetime import date

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from detention_notifier.models import Detention, DetentionMailer

from academics.models import Teacher, Student, AcademicYear, Term
from academics.utils import fmpxmlparser

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = "Import Courses"
    
    def add_arguments(self, parser):
        parser.add_argument('filename', metavar='FILENAME', help='The filename to process the detentions from')
    
    def handle(self, *args, **kwargs):
        logger.info("Beginning detention import routine")
        
        data = fmpxmlparser.parse_from_file(kwargs['filename'])

        results = data['results']    
        
        seen_ids = set()
        
        with transaction.atomic():
            detention_mailer = DetentionMailer.objects.get()
            skip_processing_before = detention_mailer.skip_processing_before
            
            for row in results:
                fields = row['parsed_fields']
                
                incident_id = fields['IDINCIDENT']
                detention_date = fields['Det Date']
                code = fields['Code']
                offense = fields['Offense']
                comments = fields['Comments']
                student_id = fields['IDSTUDENT']
                teacher_id = fields['Session.SelectedTeacher::IDTEACHER']
                raw_academic_year = fields['AcademicYear']
                raw_term = fields['Term']
                
                try:
                    academic_year = AcademicYear.objects.get(year=raw_academic_year)
                except AcademicYear.DoesNotExist:
                    academic_year = AcademicYear(year=raw_academic_year)
                    academic_year.save()
                
                try:
                    term = Term.objects.get(academic_year=academic_year, term=raw_term)
                except Term.DoesNotExist:
                    term = Term(academic_year=academic_year, term=raw_term)
                    term.save()
                
                if skip_processing_before and detention_date < skip_processing_before:
                    continue
                
                if teacher_id:
                    teacher = Teacher.objects.get(teacher_id=teacher_id)
                else:
                    teacher = None
                    
                
                if student_id:
                    student = Student.objects.get(student_id=student_id)
                else:
                    student = None
                
                if not incident_id:
                    logger.error("Blank incident ID")
                    continue
                
                seen_ids.add(incident_id)
                
                try:
                    incident = Detention.objects.get(incident_id=incident_id)
                    logger.info("Found detention {id:}".format(id=incident_id))
                    force_save = False
                    
                except Detention.DoesNotExist:
                    logger.info("Creating detention {id:}".format(id=incident_id))
                    incident = Detention(incident_id=incident_id)
                    force_save = True
                    
                attr_map = {
                    'detention_date': detention_date,
                    'code': code,
                    'offense': offense,
                    'comments': comments,
                    'term': term,
                    'student': student,
                    'teacher': teacher,
                }
                
                for attr in attr_map:
                    db_value = getattr(incident, attr)
                    
                    if db_value != attr_map[attr]:
                        setattr(incident, attr, attr_map[attr])
                        logger.info("Updating {attr:} on {incident_id:} from {old_value:} to {new_value:}".format(
                            attr=attr, incident_id=incident_id, old_value=db_value, new_value=attr_map[attr]))
                        force_save = True
                    
                if force_save:
                    incident.save()
