#!/usr/bin/python

import email.utils

from django.db import models
from django.core.urlresolvers import reverse

from polymorphic import PolymorphicModel
from adminsortable.models import SortableMixin
from adminsortable.fields import SortableForeignKey

from django.template import Template, Context
from django.core.mail import EmailMessage

from academics.models import Student, Teacher, AcademicYear, Enrollment, Course, Section, Dorm
import courseevaluations.managers

class QuestionSet(models.Model):
    name = models.CharField(max_length=255, unique=True)
    
    def __str__(self):
        return self.name

class FreeformQuestion(SortableMixin):
    question = models.CharField(max_length=255)
    question_set = SortableForeignKey(QuestionSet)
    required = models.BooleanField(default=False)
    
    question_order = models.PositiveIntegerField(default=0, editable=False, db_index=True)
    order_field_name = 'question_order'
    
    class Meta:
        ordering = ['question_order']

    def __str__(self):
        return self.question
    
class MultipleChoiceQuestion(SortableMixin):
    question = models.CharField(max_length=255)
    question_set = SortableForeignKey(QuestionSet)
    required = models.BooleanField(default=True)
    
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
    name = models.CharField(max_length=255, unique=True)
    available_until = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    objects = courseevaluations.managers.EvaluationSetManager()
    
    class Meta:
        permissions = (
        ("can_view_status_reports", "Can view status reports"),
        ("can_view_student_links", "Can view student links"),
        ("can_send_emails", "Can send e-mails"),
        )
        
        ordering = ['created_at']
    
    def __str__(self):
        return self.name
    
class Evaluable(PolymorphicModel):
    evaluation_type_label = "misc evaluation"
    evaluation_type_label_plural = "misc evaluations"
    
    evaluation_type_title = "Misc Evaluation"
    evaluation_type_title_plural = "Misc Evaluations"
    
    evaluation_set = models.ForeignKey(EvaluationSet)
    question_set = models.ForeignKey(QuestionSet)
    student = models.ForeignKey(Student)
    complete = models.BooleanField(default=False)
    
    @property
    def student_display(self):
        return None
    
class DormEvaluation(Evaluable):
    evaluation_type_label = "dorm evaluation"
    evaluation_type_label_plural = "dorm evaluations"
    
    evaluation_type_title = "Dorm Evaluation"
    evaluation_type_title_plural = "Dorm Evaluations"
    
    dorm = models.ForeignKey(Dorm)
    
    @property
    def student_display(self):
        return str(self.dorm)
    
class DormParentEvaluation(DormEvaluation):    
    evaluation_type_label = "dorm parent evaluation"
    evaluation_type_label_plural = "dorm parent evaluations"
    
    evaluation_type_title = "Dorm Parent Evaluation"
    evaluation_type_title_plural = "Dorm Parent Evaluations"
    
    parent = models.ForeignKey(Teacher)
    
    def __str__(self):
        return "{student:}: {dorm:} w/ {parent:}".format(student=self.student, dorm=self.dorm, parent=self.parent)
    
    @property
    def student_display(self):
        return "{dorm:} with {parent:}".format(dorm=str(self.dorm), parent=self.parent.name_for_students)
        
class CourseEvaluation(Evaluable):
    evaluation_type_label = "course evaluation"
    evaluation_type_label_plural = "course evaluations"
    
    evaluation_type_title = "Course Evaluation"
    evaluation_type_title_plural = "Course Evaluations"
    
    section = models.ForeignKey(Section)
    
    def __str__(self):
        return "{student:}: {section:}".format(section=self.section, student=self.student)
    
    @property
    def student_display(self):
        if self.section.teacher:
            return "{course:} with {teacher:}".format(course=self.section.course.course_name, teacher=self.section.teacher.name_for_students)
        else:
            return "{course:}".format(course=self.section.course.course_name)
        
class IIPEvaluation(Evaluable):
    evaluation_type_label = "IIP evaluation"
    evaluation_type_label_plural = "IIP evaluations"
    
    evaluation_type_title = "IIP Evaluation"
    evaluation_type_title_plural = "IIP Evaluations"
    
    teacher = models.ForeignKey(Teacher)
    
    class Meta:
        verbose_name = 'IIP evaluation'
    
    def __str__(self):
        return "{teacher:} w/ {student:}".format(teacher=self.teacher.name, student=self.student.name)
    
    @property
    def student_display(self):
        return "IIP with {teacher:}".format(teacher=self.teacher.name_for_students)
    
class MultipleChoiceQuestionAnswer(models.Model):
    evaluable = models.ForeignKey(Evaluable)
    answer = models.ForeignKey(MultipleChoiceQuestionOption)
    
class FreeformQuestionAnswer(models.Model):
    evaluable = models.ForeignKey(Evaluable)
    question = models.ForeignKey(FreeformQuestion)
    answer = models.TextField()

class StudentEmailTemplate(models.Model):
    CONTENT_SUBTYPE_CHOICES = (('html', 'HTML'), ('plain', 'Plain Text'))
    CONTENT_SUBTYPE_LENGTH = max(len(choice[0]) for choice in CONTENT_SUBTYPE_CHOICES)

    description = models.CharField(max_length=50)
    
    subject = models.CharField(max_length=254)
    body = models.TextField()
    
    from_name = models.CharField(max_length=254)
    from_address = models.EmailField(max_length=254)
    
    content_subtype = models.CharField(max_length=CONTENT_SUBTYPE_LENGTH, choices=CONTENT_SUBTYPE_CHOICES, default="plain")

    def get_template_vars(self, student):
        try:
            return self._template_vars
        except AttributeError:
            pass
        
        evaluation_sets = EvaluationSet.objects.open()
        
        complete_evaluations = Evaluable.objects.filter(evaluation_set__in=evaluation_sets, student=student, complete=True)
        incomplete_evaluations = Evaluable.objects.filter(evaluation_set__in=evaluation_sets, student=student, complete=False)
        evaluations = Evaluable.objects.filter(evaluation_set__in=evaluation_sets, student=student)
        evaluation_landing_page = "https://apps.rectoryschool.org{url:}?auth_key={auth_key:}".format(url=reverse('courseevaluations_student_landing'), auth_key=student.auth_key)
        
        template_vars = {
            'student': student,
            'complete_evaluations': complete_evaluations,
            'incomplete_evaluations': incomplete_evaluations,
            'evaluations': evaluations,
            'evaluation_landing': evaluation_landing_page
        }
        
        self._template_vars = template_vars
        
        return template_vars
    
    def render_body(self, student):
        template = Template(self.body)
        template_vars = self.get_template_vars(student)
        
        return template.render(Context(template_vars))
    
    def render_subject(self, student):
        template = Template(self.subject)
        template_vars = self.get_template_vars(student)
        
        return template.render(Context(template_vars))
 
    def get_message(self, student):
        m = EmailMessage()
        m.subject = self.render_subject(student)
        m.body = self.render_body(student)
        m.from_email = email.utils.formataddr((self.from_name, self.from_address))
        m.to = [student.email]
        m.content_subtype = self.content_subtype

        return m
            
    def __str__(self):
        return self.description
