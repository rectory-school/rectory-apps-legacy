#!/usr/bin/python

import logging
from datetime import date

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from validate_email import validate_email

from academics.models import Course
from academics.utils import fmpxmlparser

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = "Import Courses"
    
    def add_arguments(self, parser):
        parser.add_argument('filename', metavar='FILENAME', help='The filename to process the courses from')
    
    def handle(self, *args, **kwargs):
        logger.info("Beginning course import routine")
        
        data = fmpxmlparser.parse_from_file(kwargs['filename'])

        results = data['results']    
        
        seen_ids = set()
        
        with transaction.atomic():
            for row in results:
                fields = row['parsed_fields']
                
                course_number = fields['CourseNumber']
                course_name = fields['CourseName'] or ""
                course_name_short = fields["CourseNameShort"] or ""
                course_name_transcript = fields["CourseNameTranscript"] or ""
                division = fields["Division"] or ""
                grade_level = fields["GradeLevel"] or ""
                department = fields["DepartmentName"] or ""
                course_type = fields["CourseType"] or ""
                
                if not course_number:
                    continue
                
                seen_ids.add(course_number)
                
                try:
                    course = Course.objects.get(number=course_number)
                    logger.info("Found course {number:}".format(number=course_number))
                    forceSave = False
                    
                except Course.DoesNotExist:
                    course = Course(number=course_number)
                    logger.info("Creating course {number:}".format(number=course_number))
                    forceSave = True
                    
                attrMap = {
                    'course_name': course_name,
                    'course_name_short': course_name_short,
                    'course_name_transcript': course_name_transcript,
                    'division': division,
                    'grade_level': grade_level,
                    'department': department,
                    'course_type': course_type,
                }
                
                for attr in attrMap:
                    dbValue = getattr(course, attr)
                    
                    if dbValue != attrMap[attr]:
                        setattr(course, attr, attrMap[attr])
                        logger.info("Updating {attr:} on {course:} from {oldValue:} to {newValue:}".format(attr=attr, course=course_number, oldValue=dbValue, newValue=attrMap[attr]))
                        forceSave = True
                    
                if forceSave:
                    course.save()
                    
            extra_courses = Course.objects.exclude(number__in=seen_ids)
            for extra_course in extra_courses:
                logger.warn("Deleting extra course {}".format(extra_course.id))
                extra_course.delete()