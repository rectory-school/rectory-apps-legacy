import logging

from django.db import models

import academics.managers

logger = logging.getLogger(__name__)
            
        
class AcademicYear(models.Model):
    year = models.CharField(max_length=9, unique=True)
    current = models.BooleanField(default=False)
    
    objects = academics.managers.AcademicYearManager()
    
    def __str__(self):
        return self.year
        
class Student(models.Model):
    #Keystone table: ksPERMRECS
    
    student_id = models.CharField(max_length=7, unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    nickname = models.CharField(max_length=255, blank=True)
    email = models.EmailField(max_length=255, blank=True)
    current = models.BooleanField(default=False)
    
    @property
    def name(self):
        if self.nickname:
            return "{first:} ({nick:}) {last:}".format(first=self.first_name, last=self.last_name, nick=self.nickname)
        
        return "{first:} {last:}".format(first=self.first_name, last=self.last_name)
        
    def __str__(self):
        return self.name

class Teacher(models.Model):
    #Keystone table: ksTEACHERS
    teacher_id = models.CharField(max_length=4)
    
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, blank=True)
    active = models.BooleanField(default=False)
    
    @property
    def name(self):
        return "{first:} {last:}".format(first=self.first_name, last=self.last_name)
    
    def __str__(self):
        return self.name
    
class Enrollment(models.Model):
    #Keystone table: ksEnrollment
    
    student = models.ForeignKey(Student)
    academic_year = models.ForeignKey(AcademicYear)
    boarder = models.BooleanField()
    dorm = models.CharField(max_length=20, blank=True)
    grade = models.CharField(max_length=2)
    division = models.CharField(max_length=2)
    section = models.CharField(max_length=1, blank=True)
    advisor = models.ForeignKey(Teacher, blank=True, null=True)
    
    objects = academics.managers.EnrollmentManager()
    
    class Meta:
        unique_together = (('student', 'academic_year'), )
    
    def __str__(self):
        return "{name:} ({year:})".format(name=self.student.name, year=self.academic_year.year)
    
class Course(models.Model):
    #Keystone table: ksCOURSES
    
    number = models.IntegerField(unique=True)
    course_name = models.CharField(max_length=255)
    course_name_short = models.CharField(max_length=255)
    course_name_transcript = models.CharField(max_length=255)
    division = models.CharField(max_length=2)
    grade_level = models.CharField(max_length=2, blank=True)
    department = models.CharField(max_length=255)
    course_type = models.CharField(max_length=255)

class Section(models.Model):
    #Keystone table: ksSECTIONS
    
    course = models.ForeignKey(Course)
    csn = models.CharField(max_length=255)
    academic_year = models.ForeignKey(AcademicYear)
    teacher = models.ForeignKey(Teacher, blank=True, null=True)
    
    def __str__(self):
        return "{csn:} {year:}".format(csn=self.csn, year=self.academic_year.year)