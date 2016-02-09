#!/usr/bin/python

import csv
import logging
from datetime import date

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from validate_email import validate_email

from enrichmentmanager.models import Teacher, EnrichmentSlot, EnrichmentOption, EnrichmentSignup

logger = logging.getLogger("main")

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
                teacher_id, firstName, lastName, email, defaultRoom, activeEmployee, defaultDescription = map(str.strip, row)
                
                if not teacher_id:
                    continue
                
                if activeEmployee in ("1", 1):
                    activeEmployee = True
                else:
                    activeEmployee = False
                
                if email:
                    validEmail = validate_email(email)
                
                    if not validEmail:
                        email = ""
                        logger.warn("E-mail address {} for {} {} is invalid; address blanked".format(email, firstName, lastName))
                
                #Knock default room out for active employees so that enrichment options will be automatically deleted.
                if not activeEmployee:
                    defaultRoom = ""
                
                try:
                    teacher = Teacher.objects.get(teacher_id=teacher_id)
                    logger.info("Found teacher {} ({} {})".format(teacher_id, firstName, lastName))
                    forceSave = False
                    
                    currentDefaultRoom = teacher.default_room
                    currentDefaultDescription = teacher.default_description
                    
                    if teacher.first_name != firstName:
                        logger.info("Updating first_name from {} to {}".format(teacher.first_name, firstName))
                        teacher.first_name = firstName
                        forceSave = True
                    
                    if teacher.last_name != lastName:
                        logger.info("Updating last_name from {} to {}".format(teacher.last_name, lastName))
                        teacher.last_name = lastName
                        forceSave = True
                    
                    if teacher.email != email:
                        logger.info("Updating email from {} to {}".format(teacher.email, email))
                        teacher.email = email
                        forceSave = True
                    
                    if teacher.default_room != defaultRoom:
                        logger.info("Updating default room from {} to {}".format(teacher.default_room, defaultRoom))
                        teacher.default_room = defaultRoom
                        forceSave = True
                    
                    if teacher.default_description != defaultDescription:
                        logger.info("Updating default description from {} to {}".format(teacher.default_description, defaultDescription))
                        teacher.default_description = defaultDescription
                        forceSave = True
                    
                    if forceSave:
                        teacher.save()
                        
                except Teacher.DoesNotExist:
                    logger.info("Creating teacher {} ({} {})".format(teacher_id, firstName, lastName))
                    
                    teacher = Teacher(teacher_id=teacher_id)
                    teacher.first_name = firstName
                    teacher.last_name = lastName
                    teacher.email = email
                    teacher.default_room = defaultRoom
                    teacher.default_description = defaultDescription
                    
                    currentDefaultRoom = ""
                    currentDefaultDescription = ""
                    
                    teacher.save()
                
                
                logger.debug("currentDefaultRoom is {}, defaultRoom is {}".format(currentDefaultRoom, defaultRoom))
                logger.debug("currentDefaultDescription is {}, defaultDescription is {}".format(currentDefaultDescription, defaultDescription))
                
                #Handle description change
                if currentDefaultDescription != defaultDescription:
                    logger.info("Updating default enrichment description")
                    #Change the room number only where it was already the default
                    count = EnrichmentOption.objects.filter(description=currentDefaultDescription, teacher=teacher, slot__date__gt=date.today()).update(description=defaultDescription)
                    logger.debug("Total updated enrichment option count is {}".format(count))
                
                #Handle no enrichment option to enrichment option
                if not currentDefaultRoom and defaultRoom:    
                    logger.info("Creating all enrichment options")
                    
                    for slot in EnrichmentSlot.objects.filter(date__gte=date.today()):
                        existingOption = EnrichmentOption.objects.filter(slot=slot, teacher=teacher).first()
                        
                        if not existingOption:
                            option = EnrichmentOption()
                            option.slot = slot
                            option.teacher = teacher
                            option.location = defaultRoom
                            option.description = defaultDescription
                            
                            option.save()
                
                #Handle enrichment to no enrichment
                elif not defaultRoom and currentDefaultRoom:
                    logger.info("Deleting all enrichment options")
                    #Do not delete enrichment options if a description is set, indicating a special event.
                    #Blow away signups when deleting the option
                    matchedOptions = EnrichmentOption.objects.filter(description=defaultDescription, teacher=teacher, slot__date__gt=date.today(), students=None)
                    matchedSignups = EnrichmentSignup.objects.filter(enrichment_option__in=matchedOptions)
                    matchedSignups.delete()
                    matchedOptions.delete()
                
                #Handle enrichment location change
                elif defaultRoom and currentDefaultRoom and defaultRoom != currentDefaultRoom:
                    logger.info("Updating default enrichment location")
                    #Change the room number only where it was already the default
                    count = EnrichmentOption.objects.filter(location=currentDefaultRoom, teacher=teacher, slot__date__gt=date.today()).update(location=defaultRoom)
                    logger.debug("Total updated enrichment option count is {}".format(count))
                
            
        f.close()
