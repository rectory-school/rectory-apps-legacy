#!/usr/bin/python

import logging
from datetime import date

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from validate_email import validate_email

from academics.models import Section, AcademicYear, StudentRegistration, Student
from academics.utils import fmpxmlparser

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = "Import Student Registrations"
    
    def add_arguments(self, parser):
        parser.add_argument('filename', metavar='FILENAME', help='The filename to process the student registrations from')
    
    def handle(self, *args, **kwargs):
        logger.info("Beginning student registration import routine")
        
        data = fmpxmlparser.parse_from_file(kwargs['filename'])

        results = data['results']    
        
        seen_ids = set()
        
        with transaction.atomic():
            for row in results:
                fields = row['parsed_fields']
                
                csn = fields['CSN']
                academic_year = fields["AcademicYear"]
                student_id = fields["IDStudent"]
                student_reg_id = fields["IDSTUDENTREG"]
                
                if not csn or not academic_year or not student_id or not student_reg_id:
                    continue
                
                try:
                    academic_year = AcademicYear.objects.get(year=academic_year)
                except AcademicYear.DoesNotExist:
                    academic_year = AcademicYear(year=academic_year)
                    academic_year.save()
                
                try:
                    section = Section.objects.get(csn=csn, academic_year=academic_year)
                except Section.DoesNotExist:
                    logger.error("Section {csn:}/{year:} is in studentreg but not in sections".format(csn=csn, year=academic_year))
                    continue
                
                try:
                    student = Student.objects.get(student_id=student_id)
                except Student.DoesNotExist:
                    logger.error("Student {id:} is in studentreg but not in students".format(id=student_id))
                    continue
                
                try:
                    student_registration = StudentRegistration.objects.get(student_reg_id=student_reg_id)
                    logger.info("Found student registration {id:}".format(id=student_reg_id))
                    forceSave = False
                    
                except StudentRegistration.DoesNotExist:
                    student_registration = StudentRegistration(student_reg_id=student_reg_id, section=section, student=student)    
                    forceSave = True
                
                attrMap = {
                    'student': student,
                    'section': section
                }
                
                for attr in attrMap:
                    dbValue = getattr(student_registration, attr)
                    
                    if dbValue != attrMap[attr]:
                        setattr(student_registration, attr, attrMap[attr])
                        logger.info("Updating {attr:} on {student_registration:} from {oldValue:} to {newValue:}".format(attr=attr, student_registration=student_registration.student_registration_id, oldValue=dbValue, newValue=attrMap[attr]))
                        forceSave = True
                
                seen_ids.add(student_reg_id)
                    
                if forceSave:
                    student_registration.save()
            
            extra_student_registrations = StudentRegistration.objects.exclude(student_reg_id__in=seen_ids)
            for extra_student_registration in extra_student_registrations:
                logger.warn("Deleting extra student registration {}".format(extra_student_registration.student_reg_id))
                extra_student_registration.delete()