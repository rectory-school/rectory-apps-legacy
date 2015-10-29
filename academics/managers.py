import logging

from django.db import models

import academics.models

logger = logging.getLogger(__name__)

class AcademicYearManager(models.Manager):
    def current(self):
        try:
            return self.get(current=True)
        except academics.models.AcademicYear.DoesNotExist as e:
            logger.error(e)
            
            o = self.order_by('-year').first()
            if not o:
                raise academics.models.AcademicYear.DoesNotExist()
            
            return o
            
        except academics.models.AcademicYear.MultipleObjectsReturned as e:
            logger.error(e)
            return self.filter(current=True).order_by('-year').first()

class EnrollmentManager(models.Manager):
    def get_queryset(self):
        return super(EnrollmentManager, self).get_queryset().select_related('student', 'academic_year')