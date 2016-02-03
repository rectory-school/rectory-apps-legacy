#!/usr/bin/python

import logging
from datetime import date

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from validate_email import validate_email

from academics.models import Enrollment, AcademicYear
from seating_charts.models import SeatingStudent

logger = logging.getLogger(__name__)

class Command(BaseCommand):
  help = "Sync academic students with seating students"
  
  def handle(self, *args, **kwargs):
    academic_year = AcademicYear.objects.current()
    current_enrollments = Enrollment.objects.filter(student__current=True, academic_year=academic_year)
    
    for enrollment in current_enrollments:
      #Get the seating student based on the student, not the enrollment
      try:
        seating_student = SeatingStudent.objects.get(enrollment__student=enrollment.student)
        
        #We found a seating student, but the enrollment was incorrect
        if seating_student.enrollment != enrollment:
          seating_student.enrollment = enrollment
          seating_student.save()
          
      except SeatingStudent.DoesNotExist:
        #We did not find a seating student
        seating_student = SeatingStudent()
        seating_student.enrollment = enrollment
        seating_student.save()
    
