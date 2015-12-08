#!/usr/bin/python

import logging
from datetime import date

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from academics.models import Student, Teacher
from courseevaluations.models import EvaluationSet, QuestionSet, IIPEvaluation
from academics.utils import fmpxmlparser

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = "Import IIP Evaluations"
    
    def add_arguments(self, parser):
        parser.add_argument('iipfile', metavar='COURSEFILENAME', help='The filename to process the IIP mappings from')
        parser.add_argument('evaluationset', metavar='EVALUATIONSET', help='The name of the evaluation set to use')
        parser.add_argument('questionset', metavar='QUESTIONSET', help='The name of the question set to use')
        
    def handle(self, *args, **kwargs):
        logger.info("Beginning IIP import routine")
        
        data = fmpxmlparser.parse_from_file(kwargs['iipfile'])
        results = data['results']
        
        with transaction.atomic():
            evaluation_set = EvaluationSet.objects.get(name=kwargs['evaluationset'])
            question_set = QuestionSet.objects.get(name=kwargs['questionset'])
            
            for row in results:
                fields = row['parsed_fields']
                
                student_id = fields['IDStudent']
                teacher_id = fields['SectionTeacher::IDTEACHER']
                
                student = Student.objects.get(student_id=student_id)
                teacher = Teacher.objects.get(teacher_id=teacher_id)
                
                evaluable = IIPEvaluation()
                evaluable.student = student
                evaluable.teacher = teacher
                evaluable.evaluation_set = evaluation_set
                evaluable.question_set = question_set
                
                evaluable.save()