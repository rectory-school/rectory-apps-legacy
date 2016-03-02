#!/usr/bin/python

import logging
from datetime import date

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.core.mail import send_mail

from detention_notifier.models import Detention, DetentionMailer, Offense, Code, DetentionErrorNotification

from academics.models import Teacher, Student, AcademicYear, Term
from academics.utils import fmpxmlparser

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = "Import Detentions"
    
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
                raw_code = fields['Code'] or ""
                raw_offense = fields['Offense']
                comments = fields['Comments'] or ""
                student_id = fields['IDSTUDENT']
                teacher_id = fields['KSTeachers::IDTEACHER']
                raw_academic_year = fields['AcademicYear']
                raw_term = fields['Term']
                
                if skip_processing_before and detention_date < skip_processing_before:
                    continue
                
                try:
                    code = Code.objects.get(code=raw_code)
                except Code.DoesNotExist:
                    code = Code(code=raw_code)
                    code.save()
                
                if not code.process:
                    continue
                
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
                
                if raw_offense:
                    try:
                        offense = Offense.objects.get(offense__iexact=raw_offense)
                    except Offense.DoesNotExist:
                        error_recipients = [o.address for o in DetentionErrorNotification.objects.filter(mailer=detention_mailer)]
                    
                        if not error_recipients:
                            raise ValueError("No error recipients are defined")
                    
                        send_mail("Error importing detention", "Error importing detention {id:}: offense '{offense:}' does not exist".format(
                            id=incident_id, offense=raw_offense), 'technology@rectoryschool.org', error_recipients)
                    
                        continue
                else:
                    offense = None
                
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
                    incident = Detention(
                                        incident_id=incident_id,
                                        code=code,
                                        student=student,
                                        teacher=teacher
                                        )
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
                
            
            extra_detentions = Detention.objects.exclude(incident_id__in=seen_ids)
            if extra_detentions:
                logger.warn("Deleting {} detentions".format(extra_detentions.count()))
                extra_detentions.delete()