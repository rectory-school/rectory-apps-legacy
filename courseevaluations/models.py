#!/usr/bin/python

from django.db import models

from polymorphic import PolymorphicModel
from adminsortable.models import SortableMixin
from adminsortable.fields import SortableForeignKey

from academics.models import Student, Teacher, AcademicYear, Enrollment, Course, Section, Dorm

class QuestionSet(models.Model):
    name = models.CharField(max_length=255)
    
    def __str__(self):
        return self.name

class FreeformQuestion(SortableMixin):
    question = models.CharField(max_length=255)
    question_set = SortableForeignKey(QuestionSet)
    
    question_order = models.PositiveIntegerField(default=0, editable=False, db_index=True)
    order_field_name = 'question_order'
    
    class Meta:
        ordering = ['question_order']

    def __str__(self):
        return self.question
    
class MultipleChoiceQuestion(SortableMixin):
    question = models.CharField(max_length=255)
    question_set = SortableForeignKey(QuestionSet)
    
    question_order = models.PositiveIntegerField(default=0, editable=False, db_index=True)
    order_field_name = 'question_order'
    
    class Meta:
        ordering = ['question_order']
    
    def __str__(self):
        return self.question
    
class MultipleChoiceQuestionOption(SortableMixin):
    question = SortableForeignKey(MultipleChoiceQuestion)
    option = models.CharField(max_length=255)

    option_order = models.PositiveIntegerField(default=0, editable=False, db_index=True)
    order_field_name = 'option_order'
    
    class Meta:
        ordering = ['option_order']
    
    def __str__(self):
        return self.option

class EvaluationSet(models.Model):
    name = models.CharField(max_length=255)
    available_until = models.DateField()
    
    def __str__(self):
        return self.name
    
class Evaluable(PolymorphicModel):
    evaluation_type_label = "misc evaluation"
    evaluation_type_label_plural = "misc evaluations"
    
    evaluation_set = models.ForeignKey(EvaluationSet)
    question_set = models.ForeignKey(QuestionSet)
    students = models.ManyToManyField(Student)

class DormEvaluation(Evaluable):
    evaluation_type_label = "dorm evaluation"
    evaluation_type_label_plural = "dorm evaluations"
    
    dorm = models.ForeignKey(Dorm)
    
class DormParentEvaluation(DormEvaluation):    
    evaluation_type_label = "dorm parent evaluation"
    evaluation_type_label_plural = "dorm parent evaluations"
    
    parent = models.ForeignKey(Teacher)

class CourseEvaluation(Evaluable):
    evaluation_type_label = "course evaluation"
    evaluation_type_label_plural = "course evaluations"
    
    section = models.ForeignKey(Section)
    
class IIPEvaluation(Evaluable):
    evaluation_type_label = "IIP evaluation"
    evaluation_type_label_plural = "IIP evaluations"
    
    teacher = models.ForeignKey(Teacher)
    
    def __str__(self):
        return "IIP Evaluation: {name:}".format(name=self.teacher.name)

class MultipleChoiceQuestionAnswer(models.Model):
    answer = models.ForeignKey(MultipleChoiceQuestionOption)
    evaluable = models.ForeignKey(Evaluable)
    student = models.ForeignKey(Student)
    
class FreeformQuestionAnswer(models.Model):
    answer = models.TextField()
    evaluable = models.ForeignKey(Evaluable)
    question = models.ForeignKey(FreeformQuestion)