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
        parser.add_argument('filename', metavar='FILENAME', help='The filename to process the students from')
    
    def handle(self, *args, **kwargs):
        f = open(kwargs['filename'])
        
        reader = csv.reader(f)
        
        seenStudents = set()
        
        for row in reader:
            if not row:
                continue
                
            studentID, email, firstName, lastName, nickname, advisorID = map(str.strip, row)

            seenStudents.add(studentID)

            validEmail = validate_email(email)
            
            if not validEmail:
                logger.error("E-mail address {} is invalid; address blanked".format(email))
                email = ""
            
            advisor = Teacher.objects.filter(teacher_id=advisorID).first()
            
            if not advisor:
                logger.error("Advisor {} for student {} is not found; student not imported".format(advisorID, studentID))
                continue
            
            try:
                student = Student.objects.get(student_id=studentID)
                logger.info("Found student {} ({})".format(studentID, student.name))
                
                forceSave = False
                
                if student.email != email:
                    logger.info("Updating email from {} to {}".format(student.email, email))
                    student.email = email
                    forceSave = True
                
                if student.first_name != firstName:
                    logger.info("Updating first_name from {} to {}".format(student.first_name, firstName))
                    student.first_name = firstName
                    forceSave = True
                
                if student.last_name != lastName:
                    logger.info("Updating last_name from {} to {}".format(student.last_name, lastName))
                    student.last_name = lastName
                    forceSave = True
                
                if student.nickname != nickname:
                    logger.info("Updating nickname from {} to {}".format(student.nickname, nickname))
                    student.nickname = nickname
                    forceSave = True
                
                if student.advisor != advisor:
                    logger.info("Updating advisor from {} to {}".format(student.advisor.id, advisor.id))
                    student.advisor = advisor
                    forceSave = True
                
                if forceSave:
                    student.save()
                    
            except Student.DoesNotExist:
                logger.info("Creating student {} ({} {})".format(studentID, firstName, lastName))
                
                student = Student(student_id=studentID)
                student.email = email
                student.first_name = firstName
                student.last_name = lastName
                student.nickname = nickname
                student.advisor = advisor
                
                student.save()
        
        deletedStudents = Student.objects.exclude(student_id__in=seenStudents)
        for student in deletedStudents:
            logger.info("Deleting student {} ({})".format(student.student_id, student.name))
            student.delete()
        
        f.close()