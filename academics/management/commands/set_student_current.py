#!/usr/bin/python

import logging
from datetime import date

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from academics.models import Student, Enrollment, AcademicYear

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = "Import reset student's current status"
    
    def handle(self, *args, **kwargs):
        logger.info("Beginning student status reset routing")
        
        with transaction.atomic():
            Student.objects.update(current=False)
            
            current_enrollments = Enrollment.objects.filter(academic_year=AcademicYear.objects.current(), status_enrollment="Enrolled", status_attending="Attending")
            current_students = Student.objects.filter(enrollment__in=current_enrollments)
            current_students.update(current=True)