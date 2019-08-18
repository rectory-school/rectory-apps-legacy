from django.db import models
from simple_history.models import HistoricalRecords
from django.core.exceptions import ValidationError

from adminsortable.models import SortableMixin

from academics.models import Enrollment, Grade

# Create your models here.
class Ethnicity(models.Model):
  ethnicity = models.CharField(max_length=200)
	
  history = HistoricalRecords()
	
  class Meta:
    ordering = ['ethnicity']
  
  def __str__(self):
    return self.ethnicity

class SeatingStudent(models.Model):
  ALLERGYCHOICES = (('', 'No Allergies'), ('ALLERGY', 'Allergy'), ('EPIPEN', 'Allergy (EpiPen)'))
  
  enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE)
  ethnicity = models.ForeignKey(Ethnicity, null=True, blank=True, on_delete=models.CASCADE)
  
  food_allergy = models.CharField(max_length=max([len(a[0]) for a in ALLERGYCHOICES]), 
    choices=ALLERGYCHOICES, verbose_name="Food allergy status", default="", blank=True)
  
  #Some properties so I don't have to dig 8 levels in to get basic information, 
  #also to make porting easier
  @property
  def first_name(self):
    if self.enrollment.student.nickname:
      return self.enrollment.student.nickname
      
    return self.enrollment.student.first_name
  
  @property
  def last_name(self):
    return self.enrollment.student.last_name
  
  @property
  def gender(self):
    return self.enrollment.student.gender

  @property
  def flaggedName(self):    
    if self.food_allergy == "ALLERGY":
      template = "{first:} {last:}**"
    elif self.food_allergy == "EPIPEN":
      template = "{first:} {last:}**E"
    else:
      template = "{first:} {last:}"
    
    return template.format(first=self.first_name, last=self.last_name)
    
  class Meta:
    ordering = ['enrollment__student__last_name', 'enrollment__student__first_name']
  
  def __str__(self):
    return str(self.enrollment.student)

class MealTime(SortableMixin):
    name = models.CharField(max_length=200)

    history = HistoricalRecords()
    
    include_grades = models.ManyToManyField(Grade)
    
    include_boarding_students = models.BooleanField(default=False)
    include_day_students = models.BooleanField(default=False)
    
    order = models.PositiveIntegerField(default=0, editable=False, db_index=True)
    
    class Meta:
      ordering = ['order']
    
    def allStudents(self):
      students = SeatingStudent.objects.filter(enrollment__grade__in=self.include_grades.all())
      
      #Boarding only
      if self.include_boarding_students and not self.include_day_students:
        #Exclude day students
        students = students.exclude(enrollment__boarder=False)
      
      #Day only
      elif not self.include_boarding_students and self.include_day_students:
        #Exclude boarding students
        students = students.exclude(enrollment__boarder=True)
      
      #No students
      elif not self.include_boarding_students and not self.include_day_students:
        students = None
      
      #Boarding and day students, existing queryset
      else:
        pass
      
      return students
          
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
    table = models.ForeignKey(Table, on_delete=models.CASCADE)
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
    student = models.ForeignKey(SeatingStudent, on_delete=models.CASCADE)
    table = models.ForeignKey(Table, on_delete=models.CASCADE)
    meal_time = models.ForeignKey(MealTime, on_delete=models.CASCADE)
    
    history = HistoricalRecords()

    class Meta:
        unique_together = (('student', 'meal_time'), )
        
    def __str__(self):
        return "%s to %s for %s" % (self.student.student.name, self.table.description, self.meal_time.name)     
        
class TableAssignment(models.Model):
    meal_time = models.ForeignKey(MealTime, on_delete=models.CASCADE)
    student = models.ForeignKey(SeatingStudent, on_delete=models.CASCADE)
    
    table = models.ForeignKey(Table, on_delete=models.CASCADE)
    waitor = models.BooleanField(default=False)
    
    history = HistoricalRecords()
    
    class Meta:
        unique_together = (('meal_time', 'student'), )
        
        permissions = (
            ("view_table_assignments", "Can view table assignments"),
            ("edit_table_assignments", "Can edit table assignments"),
        )

class Layout(models.Model):
    name = models.CharField(max_length=25)
    
    left_print = models.ForeignKey(MealTime, related_name="+", on_delete=models.CASCADE)
    right_print = models.ForeignKey(MealTime, blank=True, null=True, related_name="+", on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name