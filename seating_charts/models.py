from django.db import models
from simple_history.models import HistoricalRecords
from django.core.exceptions import ValidationError

from academics.models import Enrollment, Grade

# Create your models here.
class Ethnicity(models.Model):
	ethnicity = models.CharField(max_length=200)
	
	history = HistoricalRecords()
	
	def __str__(self):
		return self.ethnicity

class SeatingStudent(models.Model):
  ALLERGYCHOICES = (('', 'No Allergies'), ('ALLERGY', 'Allergy'), ('EPIPEN', 'Allergy (EpiPen)'))
  
  enrollment = models.ForeignKey(Enrollment)
  ethnicity = models.ForeignKey(Ethnicity, null=True, blank=True)
  
  food_allergy = models.CharField(max_length=max([len(a[0]) for a in ALLERGYCHOICES]), 
    choices=ALLERGYCHOICES, verbose_name="Food allergy status", default="", blank=True)
  
  class Meta:
    ordering = ['enrollment__student__last_name', 'enrollment__student__first_name']
  
  def __str__(self):
    return str(self.enrollment.student)

class MealTime(models.Model):
    name = models.CharField(max_length=200)

    history = HistoricalRecords()
    
    include_grades = models.ManyToManyField(Grade)
    
    include_boarding_students = models.BooleanField(default=False)
    include_day_students = models.BooleanField(default=False)
    
    def allStudents(self):
        #TODO: Fix querying
        students = Student.objects.all()
        
        for s in students:
            if not s.grade in self.include_grades.all():
                continue
            
            if not self.include_boarding_students and s.boarder:
                continue
                
            if not self.include_day_students and not s.boarder:
                continue
                
            yield s
    
    def __str__(self):
        return str(self.name)
        
class Table(models.Model):
    description = models.CharField(max_length=200)
    for_meals = models.ManyToManyField(MealTime)

    capacity = models.IntegerField()

    history = HistoricalRecords()

    def __str__(self):
        return "Table %s (%s)" % (self.description, ", ".join(map(str, self.for_meals.all())))
        
class SeatFiller(models.Model):
    description = models.CharField(max_length=200, blank=True)
    seats = models.IntegerField()
    table = models.ForeignKey(Table)
    meal_time = models.ManyToManyField(MealTime)
    display = models.BooleanField(default=False)
    
    def clean(self):
        if not self.seats and not self.display:
            raise ValidationError("No seats are being taken up and the entry isn't being displayed. What point does it serve?")
            
        if self.display and not self.description:
            raise ValidationError("Description must not be blank if the seat filler is being displayed")
    
    history = HistoricalRecords()
    
    def __str__(self):
        if self.description:
            return self.description
        
        if self.id:
            return "SeatFiller %d" % self.id
        
        return "SeatFiller"

class PinnedStudent(models.Model):
    student = models.ForeignKey(SeatingStudent)
    table = models.ForeignKey(Table)
    meal_time = models.ForeignKey(MealTime)
    
    history = HistoricalRecords()

    class Meta:
        unique_together = (('student', 'meal_time'), )
        
    def __str__(self):
        return "%s to %s for %s" % (self.student.student.name, self.table.description, self.meal_time.name)     
        
class TableAssignment(models.Model):
    meal_time = models.ForeignKey(MealTime)
    student = models.ForeignKey(SeatingStudent)
    
    table = models.ForeignKey(Table)
    waitor = models.BooleanField(default=False)
    
    history = HistoricalRecords()
    
    class Meta:
        unique_together = (('meal_time', 'student'), )
        
        permissions = (
            ("view", "Can view table assignments"),
            ("edit", "Can edit table assignments"),
        )

class Layout(models.Model):
    name = models.CharField(max_length=25)
    
    left_print = models.ForeignKey(MealTime, related_name="+")
    right_print = models.ForeignKey(MealTime, blank=True, null=True, related_name="+")
    
    def __str__(self):
        return self.name