#!/usr/bin/python

import logging
from datetime import date

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from academics.models import Student, Dorm, Enrollment, AcademicYear
from courseevaluations.models import EvaluationSet, QuestionSet, DormParentEvaluation
from academics.utils import fmpxmlparser

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = "Import Courses"
    
    def add_arguments(self, parser):
        parser.add_argument('evaluationset', metavar='EVALUATIONSET', help='The name of the evaluation set to use')
        parser.add_argument('questionset', metavar='QUESTIONSET', help='The name of the question set to use')
        
    def handle(self, *args, **kwargs):
        logger.info("Beginning dorm parent evaluation creation routine")
                
        with transaction.atomic():
            academic_year = AcademicYear.objects.current()
            
            evaluation_set = EvaluationSet.objects.get(name=kwargs['evaluationset'])
            question_set = QuestionSet.objects.get(name=kwargs['questionset'])
            
            enrollments = Enrollment.objects.filter(student__current=True, academic_year=academic_year).exclude(dorm=None)
            
            for enrollment in enrollments:
                student = enrollment.student
                dorm = enrollment.dorm
                heads = dorm.heads.all()
                
                for teacher in heads:
                    evaluable = DormParentEvaluation()
                    evaluable.question_set = question_set
                    evaluable.evaluation_set = evaluation_set
                    
                    evaluable.dorm = dorm
                    evaluable.parent = teacher
                    evaluable.student = student
                    evaluable.enrollment = enrollment
                    
                    evaluable.save()