import logging
from random import choice

from django.db import models
from django.conf import settings

from simple_history.models import HistoricalRecords

import academics.managers

logger = logging.getLogger(__name__)
            
def default_auth_key():
    chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    return "".join(choice(chars) for i in range(63))

class AcademicYear(models.Model):
    year = models.CharField(max_length=9, unique=True)
    current = models.BooleanField(default=False)
    
    history = HistoricalRecords()
    
    objects = academics.managers.AcademicYearManager()
    
    class Meta:
        ordering = ['year']
    
    def __str__(self):
        return self.year

class Term(models.Model):
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE)
    term = models.CharField(max_length=2)
    
    class Meta:
        ordering = ['academic_year__year', 'term']
    
    def __str__(self):
        return "{academic_year:}-{term:}".format(academic_year=self.academic_year, term=self.term)
        
class Student(models.Model):
    #Keystone table: ksPERMRECS
    
    student_id = models.CharField(max_length=7, unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    nickname = models.CharField(max_length=255, blank=True)
    email = models.EmailField(max_length=255, blank=True)
    current = models.BooleanField(default=False)
    
    auth_key = models.CharField(max_length=63, default=default_auth_key)
    
    rectory_password = models.CharField(max_length=254, blank=True)
    username = models.CharField(max_length=254, blank=True)
    
    gender = models.CharField(max_length=1, blank=True, default="")
    
    parents = models.ManyToManyField('Parent', through='StudentParentRelation', blank=True)
    
    history = HistoricalRecords()
    
    class Meta:
        ordering = ('last_name', 'first_name')
    
    @property
    def name(self):
        if self.nickname:
            return "{first:} ({nick:}) {last:}".format(first=self.first_name, last=self.last_name, nick=self.nickname)
        
        return "{first:} {last:}".format(first=self.first_name, last=self.last_name)
    
    @property
    def last_name_first(self):
        if self.nickname:
            return "{last:}, {first:} ({nickname:})".format(last=self.last_name, first=self.first_name, nickname=self.nickname)
        
        return "{last:}, {first:}".format(last=self.last_name, first=self.first_name)
        
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
    
    default_enrichment_room = models.CharField(max_length=255, blank=True)
    default_enrichment_description = models.CharField(max_length=255, blank=True)
    
    history = HistoricalRecords()
    
    class Meta:
        ordering = ['last_name', 'first_name']
    
    @property
    def name(self):
        return "{first:} {last:}".format(first=self.first_name, last=self.last_name)
    
    @property
    def name_for_students(self):
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
    
    history = HistoricalRecords()
    
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
            

class Grade(models.Model):
  SCHOOL_CHOICES = (('', '--'), ('elementary', 'Elementary School'), ('middle', 'Middle School'), ('high', 'High School'))
  SCHOOL_CHOICES_LENGTH = max(len(choice[0]) for choice in SCHOOL_CHOICES)
    
  grade = models.CharField(max_length=2, unique=True)
  description = models.CharField(max_length=63, unique=True)
  
  school = models.CharField(max_length=SCHOOL_CHOICES_LENGTH, choices=SCHOOL_CHOICES, default='', blank=True)
  
  class Meta:
    ordering = ['grade']
  
  def __str__(self):
    return self.description

class Enrollment(models.Model):
    #Keystone table: ksEnrollment
    
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE)
    boarder = models.BooleanField()
    dorm = models.ForeignKey(Dorm, blank=True, null=True, on_delete=models.CASCADE)
    grade = models.ForeignKey(Grade, null=True, on_delete=models.CASCADE)
    division = models.CharField(max_length=2)
    section = models.CharField(max_length=1, blank=True)
    advisor = models.ForeignKey(Teacher, blank=True, null=True, on_delete=models.CASCADE)
    status_enrollment = models.CharField(max_length=20, blank=True)
    status_attending = models.CharField(max_length=20, blank=True)
    
    enrolled_date = models.DateField(blank=True, null=True)
    
    history = HistoricalRecords()
    
    objects = academics.managers.EnrollmentManager()
    
    @property
    def tutor(self):
        #Force into a list
        iip_course_numbers = settings.IIP_COURSE_IDS
        
        iip_registration = StudentRegistration.objects.filter(section__academic_year=self.academic_year,
                                                              student=self.student,
                                                              section__course__number__in=iip_course_numbers).first()
        
        if iip_registration:
            return iip_registration.section.teacher
        
        return None
    
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
    grade_level = models.CharField(max_length=20, blank=True)
    department = models.CharField(max_length=255)
    course_type = models.CharField(max_length=255)
    
    history = HistoricalRecords()
    
    def __str__(self):
        return "{number:}: {name:}".format(number=self.number, name=self.course_name)

class Section(models.Model):
    #Keystone table: ksSECTIONS
    
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    csn = models.CharField(max_length=255)
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, blank=True, null=True, on_delete=models.CASCADE)
    
    #The course name that can be overridden from the original course
    course_name = models.CharField(max_length=255, blank=True)
    
    students = models.ManyToManyField(Student, through='StudentRegistration')
    
    history = HistoricalRecords()
    
    class Meta:
        unique_together = (('csn', 'academic_year'), )
    
    def __str__(self):
        return "{csn:} ({year:})".format(csn=self.csn, year=self.academic_year.year)

class StudentRegistration(models.Model):
    student_reg_id = models.CharField(max_length=20, unique=True)
    
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    
    history = HistoricalRecords()
    
    def __str__(self):
        return "{section:}: {student:}".format(section=self.section, student=self.student)
  

class Parent(models.Model):
  PARENT_ID_CHOICES = (('Pa', 'Parent A'), ('Pb', 'Parent B'))
  PARENT_ID_LENGTH = max(len(choice[0]) for choice in PARENT_ID_CHOICES)
  
  family_id = models.CharField(max_length=20)
  parent_id = models.CharField(max_length=PARENT_ID_LENGTH)
  
  full_id = models.CharField(max_length=(20 + PARENT_ID_LENGTH), unique=True)
  
  first_name = models.CharField(max_length=50, blank=True)
  last_name = models.CharField(max_length=50, blank=True)
  
  email = models.EmailField(max_length=254, blank=True)
  phone_home = models.CharField(max_length=100, blank=True)
  phone_work = models.CharField(max_length=100, blank=True)
  phone_cell = models.CharField(max_length=100, blank=True)
  
  address = models.TextField(blank=True)
  
  updated_at = models.DateTimeField(auto_now=True)
  
  history = HistoricalRecords()
  
  class Meta:
    ordering = ['last_name', 'first_name']
    permissions = (("can_download_family_data", "Can download family data"), )
    
  @property
  def name(self):
    return "{:} {:}".format(self.first_name, self.last_name)

  def __str__(self):
    return self.name
    
class StudentParentRelation(models.Model):
  student = models.ForeignKey(Student, db_index=True, on_delete=models.CASCADE)
  parent = models.ForeignKey(Parent, db_index=True, on_delete=models.CASCADE)
  
  relationship = models.CharField(max_length=20, blank=True)
  family_id_key = models.CharField(max_length=20, blank=True)
  
  parent_code = models.CharField(max_length=1, blank=True)
  
  history = HistoricalRecords()
  
  def __str__(self):
    return "{:}/{:}".format(self.student, self.parent)
  
  class Meta:
    unique_together = (('student', 'parent'), )