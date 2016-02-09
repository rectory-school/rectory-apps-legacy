#!/usr/bin/python

import csv
import logging
from datetime import date

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

import academics.models
import enrichmentmanager.models

from enrichmentmanager.models import EnrichmentSlot, EnrichmentOption, EnrichmentSignup

logger = logging.getLogger("main")

class Command(BaseCommand):
    help = "Sync Academics to Enrichment"
        
    def handle(self, *args, **kwargs):
        with transaction.atomic():
            # Sync the academic and enrichment teacher objects
            academic_teachers = academics.models.Teacher.objects.all()
            for academic_teacher in academic_teachers:
                # Either get the existing enrichment teacher or create an appropriate one
                try:
                    enrichment_teacher = enrichmentmanager.models.Teacher.objects.get(academic_teacher=academic_teacher)
                    logger.info("Matched teacher {:}".format(academic_teacher.id))
                except enrichmentmanager.models.Teacher.DoesNotExist:
                    enrichment_teacher = enrichmentmanager.models.Teacher(academic_teacher=academic_teacher)
                    enrichment_teacher.save()
            
                # Description change, update all future options matching the old description
                if academic_teacher.default_enrichment_room != enrichment_teacher.default_room:
                    previous_default = enrichment_teacher.default_description
                    new_default = academic_teacher.default_enrichment_description
                
                    matching_old_slots = EnrichmentOption.objects.filter(
                        description=previous_default, teacher=enrichment_teacher, slot__date__gt=date.today())
                
                    matching_old_slots.update(description = new_default)
                    enrichment_teacher.default_description = new_default
                    enrichment_teacher.save()
                
                # We added a default room
                if academic_teacher.default_enrichment_room and not enrichment_teacher.default_room:
                    # Create an enrichment option for all future slots, making sure that teacher doesn't already have a slot
                    
                    enrichment_teacher.default_room = academic_teacher.default_enrichment_room
                    enrichment_teacher.save()
                    
                    logger.info("Creating all enrichment options")
                
                    for slot in EnrichmentSlot.objects.filter(date__gte=date.today()):
                        # Use first so we get a None instead of an exception. If somehow there is a duplicate, 
                        # it isn't my problem here.
                        existing_option = EnrichmentOption.objects.filter(slot=slot, teacher=enrichment_teacher).first()
                    
                        if not existing_option:
                            # Create an enrichment option with all the defaults
                            option = EnrichmentOption()
                            option.slot = slot
                            option.teacher = enrichment_teacher
                            option.location = enrichment_teacher.default_room
                            option.description = enrichment_teacher.default_description
                        
                            option.save()
                
                # We removed a default room
                elif not academic_teacher.default_enrichment_room and enrichment_teacher.default_room:
                    # Remove all options that had the (new) default description and are in the future
                    logger.info("Deleting all enrichment options")
                
                    matched_options = EnrichmentOption.objects.filter(
                        description=enrichment_teacher.default_description,
                        teacher=enrichment_teacher,
                        slot__date__gt=date.today())
                    
                    matched_signups = EnrichmentSignup.objects.filter(enrichment_option__in=matched_options)
                
                    matched_signups.delete()
                    matched_options.delete()
                
                    enrichment_teacher.default_room = ""
                    enrichment_teacher.save()
            
                # Location changed
                elif academic_teacher.default_enrichment_room != enrichment_teacher.default_room:
                    matched_options = EnrichmentOption.objects.filter(
                        location=academic_teacher.default_enrichment_room,
                        teacher=enrichment_teacher,
                        slot__date__gt=date.today())
                
                    matched_options.update(location=enrichment_teacher.default_enrichment_room)
                
                    enrichment_teacher.default_room = academic_teacher.default_enrichment_room
                    enrichment_teacher.save()