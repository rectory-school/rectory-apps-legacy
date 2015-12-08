import logging

from django.db import models
from datetime import date

logger = logging.getLogger(__name__)

class EvaluationSetManager(models.Manager):
    def open(self):
        return self.filter(available_until__gte=date.today())
