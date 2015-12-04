import logging

from django.db import models

import academics.managers

logger = logging.getLogger(__name__)
            
        
class AcademicYear(models.Model):
    year = models.CharField(max_length=9, unique=True)
    current = models.BooleanField(default=False)
    
    objects = academics.managers.AcademicYearManager()
    
    class Meta:
        ordering = ['year']
    
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
    
    class Meta:
        ordering = ('last_name', 'first_name')
    
    @property
    def name(self):
        if self.nickname:
            return "{first:} ({nick:}) {last:}".format(first=self.first_name, last=self.last_name, nick=self.nickname)
        
        return "{first:} {last:}".format(first=self.first_name, last=self.last_name)
        
    def __str__(self):
        return self.name

class Teacher(models.Model):
    #Keystone table: ksTEACHERS
    teacher_id = models.CharField(max_length=5, unique=True)
    unique_name = models.CharField(max_length=255)
    
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    prefix = models.CharField(max_length=255, blank=True)
    
    email = models.EmailField(max_length=255, blank=True)
    active = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['last_name', 'first_name']
    
    @property
    def name(self):
        return "{first:} {last:}".format(first=self.first_name, last=self.last_name)
    
    @property
    def nameForStudents(self):
        if self.prefix and self.last_name:
            return "{prefix:} {last:}".format(prefix=self.prefix, last=self.last_name)
        
        elif self.first_name and self.last_name:
            return "{last:}, {first:}".format(last=self.last_name, first=self.first_name)
        
        elif self.last_name:
            return "M. {last:}".format(last=self.last_name)
        
        else:
            return "Teacher {id:}".format(id=self.teacher_id)
    
    def __str__(self):
        return self.name
    
class Dorm(models.Model):
    dorm_name = models.CharField(max_length=20, unique=True)
    
    building = models.CharField(max_length=20)
    wing = models.CharField(max_length=20, blank=True)
    level = models.CharField(max_length=20, blank=True)
    
    heads = models.ManyToManyField(Teacher, related_name="+", limit_choices_to={'active': True}, blank=True, verbose_name="dorm parents")
    
    class Meta:
        ordering = ['building', 'wing', 'level']
    
    def __str__(self):
        attrs = {'building': self.building, 'wing': self.wing, 'level': self.level}
        if self.wing and self.level:
            return "{building:} {level:} {wing:}".format(**attrs)
        
        elif self.wing:
            return "{building:} {wing:}".format(**attrs)
        
        elif self.level:
            return "{level:} {building:}".format(**attrs)
        
        else:
            return self.building
            

class Enrollment(models.Model):
    #Keystone table: ksEnrollment
    
    student = models.ForeignKey(Student)
    academic_year = models.ForeignKey(AcademicYear)
    boarder = models.BooleanField()
    dorm = models.ForeignKey(Dorm, blank=True, null=True)
    grade = models.CharField(max_length=2)
    division = models.CharField(max_length=2)
    section = models.CharField(max_length=1, blank=True)
    advisor = models.ForeignKey(Teacher, blank=True, null=True)
    status_enrollment = models.CharField(max_length=20, blank=True)
    status_attending = models.CharField(max_length=20, blank=True)
    
    objects = academics.managers.EnrollmentManager()
    
    class Meta:
        unique_together = (('student', 'academic_year'), )
        ordering = ['student__last_name', 'student__first_name', 'academic_year__year']
    
    def __str__(self):
        return "{name:} ({year:})".format(name=self.student.name, year=self.academic_year.year)

class Course(models.Model):
    #Keystone table: ksCOURSES
    
    number = models.CharField(max_length=20, unique=True)
    course_name = models.CharField(max_length=255)
    course_name_short = models.CharField(max_length=255)
    course_name_transcript = models.CharField(max_length=255)
    division = models.CharField(max_length=2)
    grade_level = models.CharField(max_length=2, blank=True)
    department = models.CharField(max_length=255)
    course_type = models.CharField(max_length=255)
    
    def __str__(self):
        return "{number:}: {name:}".format(number=self.number, name=self.course_name)

class Section(models.Model):
    #Keystone table: ksSECTIONS
    
    course = models.ForeignKey(Course)
    csn = models.CharField(max_length=255)
    academic_year = models.ForeignKey(AcademicYear)
    teacher = models.ForeignKey(Teacher, blank=True, null=True)
    
    students = models.ManyToManyField(Student, through='StudentRegistration')
    
    class Meta:
        unique_together = (('csn', 'academic_year'), )
    
    def __str__(self):
        return "{csn:} ({year:})".format(csn=self.csn, year=self.academic_year.year)

class StudentRegistration(models.Model):
    student_reg_id = models.CharField(max_length=20, unique=True)
    
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    
    def __str__(self):
        return "{section:}: {student:}".format(section=self.section, student=self.student)