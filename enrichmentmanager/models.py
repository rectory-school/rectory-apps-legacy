from django.db import models
from simple_history.models import HistoricalRecords

class EmailSuppression(models.Model):
    suppression_date = models.DateField(unique=True)
    
    def __str__(self):
        return self.suppression_date.strftime("%Y-%m-%d")

# Create your models here.
class Teacher(models.Model):
    teacher_id = models.CharField(max_length=5, unique=True)
    email = models.EmailField(max_length=254, blank=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    default_room = models.CharField(max_length=100, blank=True)
    default_description = models.CharField(max_length=100, blank=True)
    
    history = HistoricalRecords()
    
    class Meta:
        ordering = ['last_name', 'first_name']
    
    @property
    def name(self):
        return "{first} {last}".format(first=self.first_name, last=self.last_name)
        
    def __str__(self):
        return self.name

class Student(models.Model):
    student_id = models.CharField(max_length=8, unique=True)
    email = models.EmailField(max_length=254)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    nickname = models.CharField(max_length=100, blank=True)
    lockout = models.CharField(max_length=100, blank=True)
    
    advisor = models.ForeignKey(Teacher)
    associated_teachers = models.ManyToManyField(Teacher, related_name='associated_teachers', blank=True)
    
    history = HistoricalRecords()
    
    class Meta:
        ordering = ['last_name', 'first_name']
    
    @property
    def name(self):
        if self.nickname:
            return "{first} ({nickname}) {last}".format(first=self.first_name, nickname=self.nickname, last=self.last_name)
        
        return "{first} {last}".format(first=self.first_name, last=self.last_name)
        
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
    slot = models.ForeignKey(EnrichmentSlot)
    teacher = models.ForeignKey(Teacher)
    location = models.CharField(max_length=50, blank=True)
    description = models.CharField(max_length=254, blank=True)
    students = models.ManyToManyField(Student, through='EnrichmentSignup')
    
    history = HistoricalRecords()
    
    class Meta:
        unique_together = ('slot', 'teacher')
        ordering = ['teacher__last_name', 'teacher__first_name']
        
    @property
    def displayWithLocation(self):
        if self.location:
            return "{} ({})".format(str(self), self.location)
    
    def __str__(self):
        if self.description:
            return "{teacher}: {description}".format(teacher=self.teacher, description=self.description)
        
        return str(self.teacher)

#TODO: Handle slot better
class EnrichmentSignup(models.Model):
    slot = models.ForeignKey(EnrichmentSlot)
    enrichment_option = models.ForeignKey(EnrichmentOption, on_delete=models.PROTECT)
    student = models.ForeignKey(Student)
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
    
    def __str__(self):
        return "Student Signup for {name:} on {date:} with {option:}".format(name=self.student.name, date=self.slot.date.strftime("%Y-%m-%d"), option=self.enrichment_option)