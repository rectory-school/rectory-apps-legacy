#!/usr/bin/python

import logging
from datetime import date

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from validate_email import validate_email

from academics.models import Course, Section, AcademicYear, Teacher
from academics.utils import fmpxmlparser

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = "Import Sections"
    
    def add_arguments(self, parser):
        parser.add_argument('filename', metavar='FILENAME', help='The filename to process the sections from')
    
    def handle(self, *args, **kwargs):
        logger.info("Beginning section import routine")
        
        data = fmpxmlparser.parse_from_file(kwargs['filename'])

        results = data['results']    
        
        seen_ids = set()
        
        with transaction.atomic():
            for row in results:
                fields = row['parsed_fields']
                
                course_number = fields['CourseNumber']
                csn = fields['CourseSectionNumber']
                academic_year = fields["AcademicYear"]
                teacher_id = fields["IDTeacher"]
                
                if not course_number or not csn or not academic_year:
                    continue
                
                try:
                    course = Course.objects.get(number=course_number)
                    logger.info("Found course {number:}".format(number=course_number))
                    forceSave = False
                    
                except Course.DoesNotExist:
                    logger.error("Course {course:} is in sections but not courses".format(course=course_number))
                    continue
                
                try:
                    academic_year = AcademicYear.objects.get(year=academic_year)
                except AcademicYear.DoesNotExist:
                    academic_year = AcademicYear(year=academic_year)
                    academic_year.save()
                
                try:
                    section = Section.objects.get(course=course, academic_year=academic_year, csn=csn)
                    logger.info("Found section {csn:} for {academic_year:}".format(csn=csn, academic_year=academic_year))

                except Section.DoesNotExist:
                    logger.info("Creating section {csn:} for {academic_year:}".format(csn=csn, academic_year=academic_year))
                    section = Section(course=course, academic_year=academic_year, csn=csn)
                    section.save()
                
                teacher = None
                
                if teacher_id:
                    try:
                        teacher = Teacher.objects.get(teacher_id=teacher_id)
                    except Teacher.DoesNotExist:
                        logger.error("Teacher {id:} is in sections but not in teachers".format(id=teacher_id))
                    
                attrMap = {
                    'teacher': teacher,
                }
                
                for attr in attrMap:
                    dbValue = getattr(section, attr)
                    
                    if dbValue != attrMap[attr]:
                        setattr(section, attr, attrMap[attr])
                        logger.info("Updating {attr:} on {course:} from {oldValue:} to {newValue:}".format(attr=attr, course=course_number, oldValue=dbValue, newValue=attrMap[attr]))
                        forceSave = True
                    
                if forceSave:
                    section.save()
            
            #TODO: Delete extra sessions