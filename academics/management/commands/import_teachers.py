#!/usr/bin/python

import logging
from datetime import date

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from validate_email import validate_email

from academics.models import Teacher
from academics.utils import fmpxmlparser

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = "Import Teachers"
    
    def add_arguments(self, parser):
        parser.add_argument('filename', metavar='FILENAME', help='The filename to process the teachers from')
    
    def handle(self, *args, **kwargs):
        logger.info("Beginning teacher import routine")
        
        data = fmpxmlparser.parse_from_file(kwargs['filename'])

        results = data['results'] 
           
        seen_ids = set()
        
        with transaction.atomic():
            for row in results:
                fields = row['parsed_fields']
                
                nameFirst = fields['NameFirst'] or ""
                nameLast = fields['NameLast'] or ""
                namePrefix = fields['NamePrefix'] or ""
                email = fields['EmailSchool'] or ""
                activeEmployee = fields['Active Employee'] or ""
                uniqueName = fields['NameUnique'] or ""
                teacherID = fields['IDTEACHER']
                
                defaultEnrichmentRoom = fields["Enrichment Meeting Room"] or ""
                defaultEnrichmentDescription = fields["Enrichment_Description"] or ""
                
                # Preprocess the default enrichment room to be empty
                # if the employee no longer works here
                if not activeEmployee:
                    defaultEnrichmentRoom = ""
                
                if not teacherID:
                    continue
                
                seen_ids.add(teacherID)
                
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
                    'unique_name': uniqueName,
                    'default_enrichment_room': defaultEnrichmentRoom,
                    'default_enrichment_description': defaultEnrichmentDescription,
                }
                
                for attr in attrMap:
                    dbValue = getattr(teacher, attr)
                    
                    if dbValue != attrMap[attr]:
                        setattr(teacher, attr, attrMap[attr])
                        logger.info("Updating {attr:} on {teacherID:} from {oldValue:} to {newValue:}".format(attr=attr, teacherID=teacherID, oldValue=dbValue, newValue=attrMap[attr]))
                        forceSave = True
                    
                if forceSave:
                    teacher.save()
            
            extra_teachers = Teacher.objects.exclude(teacher_id__in=seen_ids)
            for extra_teacher in extra_teachers:
                logger.warn("Deleting extra teacher {}".format(extra_teacher.id))
                extra_teacher.delete()
