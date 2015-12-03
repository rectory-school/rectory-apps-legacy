#!/usr/bin/python

import csv
import logging
from datetime import date

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from validate_email import validate_email

from academics.models import Teacher

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = "Import Teachers"
    
    def add_arguments(self, parser):
        parser.add_argument('filename', metavar='FILENAME', help='The filename to process the teachers from')
    
    def handle(self, *args, **kwargs):
        logger.info("Beginning teacher import routine")
        
        f = open(kwargs['filename'])
        
        reader = csv.reader(f)
        
        with transaction.atomic():        
            for row in reader:
                nameFirst, nameLast, namePrefix, email, activeEmployee, uniqueName, teacherID = map(str.strip, row)
                print(teacherID)
                
                if not teacherID:
                    continue
                
                if activeEmployee in ("1", 1):
                    activeEmployee = True
                else:
                    activeEmployee = False
                
                if email:
                    validEmail = validate_email(email)
                
                    if not validEmail:
                        email = ""
                        logger.warn("E-mail address {email:} for {id:} ({first:} {last:}) is invalid; address blanked".format(email=email, id=teacherID, first=firstName, last=lastName))
                
                try:
                    teacher = Teacher.objects.get(teacher_id=teacherID)
                    logger.info("Found teacher {teacherID:}".format(teacherID=teacherID))
                    forceSave = False
                    
                except Teacher.DoesNotExist:
                    teacher = Teacher(teacher_id=teacherID)
                    logger.info("Creating teacher {teacherID:}".format(teacherID=teacherID))
                    forceSave = True
                    
                attrMap = {
                    'first_name': nameFirst,
                    'last_name': nameLast,
                    'prefix': namePrefix,
                    'email': email,
                    'active': activeEmployee,
                    'unique_name': uniqueName
                }
                
                for attr in attrMap:
                    dbValue = getattr(teacher, attr)
                    
                    if dbValue != attrMap[attr]:
                        setattr(teacher, attr, attrMap[attr])
                        logger.info("Updating {attr:} on {teacherID:} from {oldValue:} to {newValue:}".format(attr=attr, teacherID=teacherID, oldValue=dbValue, newValue=attrMap[attr]))
                        forceSave = True
                    
                if forceSave:
                    teacher.save()
            
        f.close()
