from django.db import models
from solo.models import SingletonModel

from academics.models import Term, Student, Teacher

class DetentionMailer(SingletonModel):
    from_name = models.CharField(max_length=255)
    from_email = models.EmailField(max_length=255)
    
    detention_protol = models.TextField()
    signature = models.TextField()
    
    skip_processing_before = models.DateField(blank=True, null=True)
    
class Offense(models.Model):
    offense = models.CharField(max_length=255, unique=True)
    sentence_insert = models.CharField(max_length=4096)
    mail = models.BooleanField(default=True)
    
    def __str__(self):
        return self.detention_reason

class Detention(models.Model):
    incident_id = models.PositiveIntegerField(unique=True)
    detention_date = models.DateField()
    code = models.CharField(max_length=254)
    offense = models.ForeignKey(Offense)
    comments = models.TextField(blank=True)
    
    term = models.ForeignKey(Term, null=True)
    student = models.ForeignKey(Student, null=True)
    teacher = models.ForeignKey(Teacher, null=True)