#!/usr/bin/python

import csv
import logging
from datetime import date

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from validate_email import validate_email

from enrichmentmanager.models import Student, Teacher

logger = logging.getLogger("main")

class Command(BaseCommand):
    help = "Import Students"
    
    def add_arguments(self, parser):
        parser.add_argument('filename', metavar='FILENAME', help='The filename to process the student registrations from')
    
    def handle(self, *args, **kwargs):
        f = open(kwargs['filename'])
        
        reader = csv.reader(f)
        
        workingAcademicYear = None
        
        #Get the latest year
        for row in reader:
            if not row:
                continue
                
            studentID, academicYear, teacherID = row
            if not workingAcademicYear or academicYear > workingAcademicYear:
                workingAcademicYear = academicYear
        
        #Reset my CSV reader
        f.seek(0)

        #Create the mapping of student ID to teacher ID
        relatedTeacherMapping = {}
        for row in reader:
            if not row:
                continue
            
            studentID, academicYear, teacherID = row
        
            #Skip any non-current years
            if academicYear != workingAcademicYear:
                continue
        
            #Skip blank teacher
            if not teacherID:
                continue
            
            if studentID not in relatedTeacherMapping:
                relatedTeacherMapping[studentID] = set()
            
            relatedTeacherMapping[studentID].add(teacherID)
        
        with transaction.atomic():
            for studentID, teacherIDs in relatedTeacherMapping.items():
                try:
                    student = Student.objects.get(student_id=studentID)
                    teachers = Teacher.objects.filter(teacher_id__in=teacherIDs)
                    student.associated_teachers = teachers
                except Student.DoesNotExist:
                    logger.warn("Student {} was in stureg but is not a student".format(studentID))
            
        f.close()