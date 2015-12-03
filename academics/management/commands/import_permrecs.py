#!/usr/bin/python

import logging
from datetime import date

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from validate_email import validate_email

from academics.models import Student
from academics.utils import fmpxmlparser

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = "Import Permrecs"
    
    def add_arguments(self, parser):
        parser.add_argument('filename', metavar='FILENAME', help='The filename to process the students from')
    
    def handle(self, *args, **kwargs):
        logger.info("Beginning student import routine")
        
        data = fmpxmlparser.parse_from_file(kwargs['filename'])

        results = data['results']    
        
        with transaction.atomic():
            for row in results:
                fields = row['parsed_fields']
                
                nameFirst = fields['NameFirst'] or ""
                nameLast = fields['NameLast'] or ""
                nameNickname = fields['NameNickname'] or ""
                email = fields['EMailSchool'] or ""
                studentID = fields['IDSTUDENT']
                
                if not studentID:
                    continue
                
                if email:
                    validEmail = validate_email(email)
                
                    if not validEmail:
                        email = ""
                        logger.warn("E-mail address {email:} for {id:} ({first:} {last:}) is invalid; address blanked".format(email=email, id=studentID, first=nameFirst, last=nameLast))
                
                try:
                    student = Student.objects.get(student_id=studentID)
                    logger.info("Found student {studentID:}".format(studentID=studentID))
                    forceSave = False
                    
                except Student.DoesNotExist:
                    student = Student(student_id=studentID)
                    logger.info("Creating student {studentID:}".format(studentID=studentID))
                    forceSave = True
                    
                attrMap = {
                    'first_name': nameFirst,
                    'last_name': nameLast,
                    'nickname': nameNickname,
                    'email': email,
                }
                
                for attr in attrMap:
                    dbValue = getattr(student, attr)
                    
                    if dbValue != attrMap[attr]:
                        setattr(student, attr, attrMap[attr])
                        logger.info("Updating {attr:} on {studentID:} from {oldValue:} to {newValue:}".format(attr=attr, studentID=studentID, oldValue=dbValue, newValue=attrMap[attr]))
                        forceSave = True
                    
                if forceSave:
                    student.save()
