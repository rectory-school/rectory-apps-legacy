from django.db import models

from adminsortable.fields import SortableForeignKey
from adminsortable.models import SortableMixin

from django.core.exceptions import ValidationError

# Create your models here.
class Calendar(models.Model):
    title = models.CharField(max_length=254)
        
    start_date = models.DateField()
    end_date = models.DateField()
    
    sunday = models.BooleanField(default=False)
    monday = models.BooleanField(default=True)
    tuesday = models.BooleanField(default=True)
    wednesday = models.BooleanField(default=True)
    thursday = models.BooleanField(default=True)
    friday = models.BooleanField(default=True)
    saturday = models.BooleanField(default=False)
    
    @property
    def numeric_days(self):
        out = []
        
        if self.monday:
            out.append(0)

        if self.tuesday:
            out.append(1)
    
        if self.wednesday:
            out.append(2)
    
        if self.thursday:
            out.append(3)
    
        if self.friday:
            out.append(4)
    
        if self.saturday:
            out.append(5)
    
        if self.sunday:
            out.append(6)
        
        return out
    
    def clean(self):
        if self.start_date > self.end_date:
            raise ValidationError("End date must be after start date")
    
    def __str__(self):
        return self.title
    
class Day(SortableMixin):
    calendar = SortableForeignKey(Calendar, on_delete=models.CASCADE)
    letter = models.CharField(max_length=1)
    
    day_order = models.PositiveIntegerField(default=0, editable=False, db_index=True)
    
    class Meta:
        ordering = ['day_order']
    
    def __str__(self):
        return self.letter

class SkipDate(models.Model):
    calendar = models.ForeignKey(Calendar, on_delete=models.CASCADE)
    date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    
    class Meta:
        unique_together=(('calendar', 'date'), )
        ordering = ['date']
    
    def clean(self):
        if self.end_date and self.date >= self.end_date:
            raise ValidationError("End date must be after start date")
    
    def __str__(self):
        return self.date.strftime("%Y-%m-%d")

class ResetDate(models.Model):
    calendar = models.ForeignKey(Calendar, on_delete=models.CASCADE)
    date = models.DateField()
    day = models.ForeignKey(Day, on_delete=models.CASCADE)
    
    