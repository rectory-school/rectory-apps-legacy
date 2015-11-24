from django.db import models

from polymorphic import PolymorphicModel
from adminsortable.models import SortableMixin
from adminsortable.fields import SortableForeignKey

from academics.models import Student, Teacher, AcademicYear, Enrollment, Course, Section, Dorm

class QuestionSet(models.Model):
    name = models.CharField(max_length=255)
    
    def __str__(self):
        return self.name
    
class MultipleChoiceQuestion(SortableMixin):
    question = models.CharField(max_length=255)
    
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

class EvaluationSet(models.Model):
    name = models.CharField(max_length=255)
    available_until = models.DateField()
    
class Evaluable(PolymorphicModel):
    evaluation_set = models.ForeignKey(EvaluationSet)
    question_set = models.ForeignKey(QuestionSet)
    students = models.ManyToManyField(Student)
    
    class Meta:
        abstract = True

class DormEvaluation(Evaluable):
    dorm = models.ForeignKey(Dorm)
    
    class Meta:
        abstract = True

class DormParentEvaluation(DormEvaluation):
    def _getAvailableParents(self):
        return self.dorm.heads.all()
    
    parent = models.ForeignKey(Teacher, limit_choices_to=_getAvailableParents)

class CourseEvaluation(Evaluable):
    section = models.ForeignKey(Section)
    
    
class IIPEvaluation(Evaluable):
    teacher = models.ForeignKey(Teacher)
    
    def __str__(self):
        return "IIP Evaluation: {name:}".format(name=self.teacher.name)