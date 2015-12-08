#!/usr/bin/python

import logging
from datetime import date

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from academics.models import Section, Course
from courseevaluations.models import EvaluationSet, QuestionSet, CourseEvaluation
from academics.utils import fmpxmlparser

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = "Import Courses"
    
    def add_arguments(self, parser):
        parser.add_argument('coursesfile', metavar='COURSEFILENAME', help='The filename to process the courses from')
        parser.add_argument('evaluationset', metavar='EVALUATIONSET', help='The name of the evaluation set to use')
        parser.add_argument('questionset', metavar='QUESTIONSET', help='The name of the question set to use')
        
    def handle(self, *args, **kwargs):
        logger.info("Beginning course import routine")
        
        data = fmpxmlparser.parse_from_file(kwargs['coursesfile'])
        results = data['results']
        
        with transaction.atomic():
            evaluation_set = EvaluationSet.objects.get(name=kwargs['evaluationset'])
            question_set = QuestionSet.objects.get(name=kwargs['questionset'])
            
            for row in results:
                fields = row['parsed_fields']
                
                csn = fields['CourseSectionNumber']
                academic_year = fields['AcademicYear']
                
                section = Section.objects.get(csn=csn, academic_year__year=academic_year)
                
                for student in section.students.all():
                    evaluable = CourseEvaluation()
                    evaluable.student = student
                    evaluable.section = section
                    evaluable.question_set = question_set
                    evaluable.evaluation_set = evaluation_set
                    evaluable.save()