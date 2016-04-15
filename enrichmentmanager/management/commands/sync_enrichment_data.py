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
            
            current_academic_year = academics.models.AcademicYear.objects.current()
            
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
                if academic_teacher.default_enrichment_description != enrichment_teacher.default_description:
                    previous_default = enrichment_teacher.default_description
                    new_default = academic_teacher.default_enrichment_description
                
                    matching_future_slots = EnrichmentOption.objects.filter(
                        description=previous_default, teacher=enrichment_teacher, slot__date__gt=date.today())
                
                    matching_future_slots.update(description = new_default)
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
                
                    matched_options.update(location=enrichment_teacher.default_room)
                
                    enrichment_teacher.default_room = academic_teacher.default_enrichment_room
                    enrichment_teacher.save()
                    
                    
            
            relevant_enrollments = academics.models.Enrollment.objects.filter(
                student__current=True, academic_year=current_academic_year, grade__school='middle').exclude(advisor=None)
                
            relevant_academic_students = academics.models.Student.objects.filter(enrollment__in=relevant_enrollments)
            
            for enrollment in relevant_enrollments:
                academic_student = enrollment.student
                
                # Get the enrichment teacher that matches the advisor in academics
                enrichment_advisor = enrichmentmanager.models.Teacher.objects.get(academic_teacher=enrollment.advisor)
                
                #Either get the enrichment student or create a new one
                try:
                    enrichment_student = enrichmentmanager.models.Student.objects.get(academic_student=academic_student)
                    if enrichment_student.advisor != enrichment_advisor:
                        enrichment_student.advisor = enrichment_advisor
                        enrichment_student.save()
                        
                except enrichmentmanager.models.Student.DoesNotExist:
                    enrichment_student = enrichmentmanager.models.Student()
                    enrichment_student.academic_student = academic_student
                    enrichment_student.advisor = enrichment_advisor
                    enrichment_student.save()
                
                #Make our way through getting to the relevant teachers
                registrations = academics.models.StudentRegistration.objects.filter(
                    student=academic_student, section__academic_year=current_academic_year)
                
                sections = academics.models.Section.objects.filter(studentregistration__in=registrations)
                academic_teachers = academics.models.Teacher.objects.filter(section__in=sections).order_by().distinct()
                enrichment_teachers = enrichmentmanager.models.Teacher.objects.filter(academic_teacher__in=academic_teachers)
                
                enrichment_student.associated_teachers = enrichment_teachers
                
            # Delete extra students
            enrichmentmanager.models.Student.objects.filter(academic_student__current=False).delete()
            
            # Teachers are not deleted because a recently fired teacher may still be indicated as the advisor for a student,
            # which is not an optional foreign key.
            