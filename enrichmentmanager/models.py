from django.db import models
from simple_history.models import HistoricalRecords

import academics.models
import enrichmentmanager.managers

class EmailSuppression(models.Model):
    suppression_date = models.DateField(unique=True)
    
    def __str__(self):
        return self.suppression_date.strftime("%Y-%m-%d")

# Create your models here.
class Teacher(models.Model):
    academic_teacher = models.ForeignKey(academics.models.Teacher, on_delete=models.CASCADE)
    
    # These are staying synthesized on this model so that I can compare
    # their old values during the teacher sync and update the enrichment
    # slots appropriately
    default_room = models.CharField(max_length=100, blank=True)
    default_description = models.CharField(max_length=100, blank=True)
    
    history = HistoricalRecords()
    
    @property
    def teacher_id(self):
        return self.academic_teacher.teacher_id
    
    @property
    def email(self):
        return self.academic_teacher.email
    
    @property
    def first_name(self):
        return self.academic_teacher.first_name
    
    @property
    def last_name(self):
        return self.academic_teacher.last_name
    
    @property
    def name(self):
        return self.academic_teacher.name
    
    class Meta:
        ordering = ['academic_teacher__last_name', 'academic_teacher__first_name']
    
    objects = enrichmentmanager.managers.TeacherManager()
        
    def __str__(self):
        return self.name

class Student(models.Model):
    # This is a proxy model for the academics student model,
    # ported from the original standalone model

    academic_student = models.ForeignKey(academics.models.Student, on_delete=models.CASCADE)
    
    lockout = models.CharField(max_length=100, blank=True)
    
    #Teacher fields are staying a foreign key to my teacher for consistency and querying
    advisor = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    associated_teachers = models.ManyToManyField(Teacher, related_name='associated_teachers', blank=True)
    
    history = HistoricalRecords()
    
    @property
    def student_id(self):
        return self.academic_student.student_id
    
    @property
    def email(self):
        return self.academic_student.email
    
    @property
    def first_name(self):
        return self.academic_student.first_name
    
    @property
    def last_name(self):
        return self.academic_student.last_name
    
    @property
    def nickname(self):
        return self.academic_student.nickname
    
    @property
    def name(self):
        return self.academic_student.name
        
    class Meta:
        pass
        ordering = ['academic_student__last_name', 'academic_student__first_name']
            
    def __str__(self):
        return self.name
    
    
class EnrichmentSlot(models.Model):
    date = models.DateField(unique=True)
    editable_until = models.DateTimeField(blank=True, null=True)
    history = HistoricalRecords()
    
    class Meta:
        ordering = ['date']
    
    def __str__(self):
        return self.date.strftime("%B %d, %Y")

class EnrichmentOption(models.Model):
    slot = models.ForeignKey(EnrichmentSlot, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    location = models.CharField(max_length=50, blank=True)
    description = models.CharField(max_length=254, blank=True)
    students = models.ManyToManyField(Student, through='EnrichmentSignup')
    
    history = HistoricalRecords()
    
    class Meta:
        unique_together = ('slot', 'teacher')
        ordering = ['teacher__academic_teacher__last_name', 'teacher__academic_teacher__first_name']
        
    @property
    def displayWithLocation(self):
        if self.location:
            return "{} ({})".format(str(self), self.location)
    
    objects = enrichmentmanager.managers.EnrichmentOptionManager()
    
    def __str__(self):
        if self.description:
            return "{teacher}: {description}".format(teacher=self.teacher, description=self.description)
        
        return str(self.teacher)

#TODO: Handle slot better
class EnrichmentSignup(models.Model):
    slot = models.ForeignKey(EnrichmentSlot, on_delete=models.CASCADE)
    enrichment_option = models.ForeignKey(EnrichmentOption, on_delete=models.PROTECT)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    details = models.CharField(max_length=255, blank=True)
    admin_lock = models.BooleanField(default=False)
    
    history = HistoricalRecords()
    
    class Meta:
        unique_together = ('slot', 'student')
        
        permissions = (
            ("can_view_own_advisees", "Can view own advisees"),
            ("can_view_other_advisees", "Can view other advisor's advisees"),
            ("can_view_all_advisees", "Can view the full advisee lists"),
            ("can_edit_own_advisees", "Can edit own advisee signups"),
            ("can_edit_all_advisees", "Can edit all advisees signups"),
            ("can_edit_same_day", "Can edit advisee signups on the same day"),
            ("can_view_reports", "Can view reports"),
            ("can_view_single_student", "Can view single student"),
            ("can_override_admin_lock", "Can override admin lock"),
            ("can_set_admin_lock", "Can set admin lock"),
        )
        
    def clean(self):
        self.slot = self.enrichment_option.slot
    
    objects = enrichmentmanager.managers.EnrichmentSignupManager()
    
    def __str__(self):
        return "Student Signup for {name:} on {date:} with {option:}".format(name=self.student.name, date=self.slot.date.strftime("%Y-%m-%d"), option=self.enrichment_option)