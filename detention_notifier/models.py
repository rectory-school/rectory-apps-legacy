from django.db import models
from django.core.exceptions import ValidationError

from solo.models import SingletonModel

from academics.models import Term, Student, Teacher

class Code(models.Model):
    code = models.CharField(max_length=255, unique=True)
    process = models.BooleanField(default=False)
    
    def __str__(self):
        return self.code

class Offense(models.Model):
    offense = models.CharField(max_length=255, unique=True)
    sentence_insert = models.CharField(max_length=4096, blank=True)
    email_listing = models.CharField(max_length=255, blank=True)
    
    mail = models.BooleanField(default=True)

    def clean(self):
        #Require a sentense_insert if mail is set to go
        
        if self.mail and not self.sentence_insert:
            raise ValidationError("Mailing offenses should have a sentense insert")
    
    def __str__(self):
        return self.offense

class DetentionMailer(SingletonModel):
    from_name = models.CharField(max_length=255)
    from_email = models.EmailField(max_length=255)
    blank_offense = models.ForeignKey(Offense, null=True, blank=True, on_delete=models.CASCADE)
    
    reply_to_from = models.BooleanField(default=True, verbose_name="Reply-to address above")
    reply_to_advisor = models.BooleanField(default=True, verbose_name="Reply-to advisor")
    reply_to_tutor = models.BooleanField(default=False, verbose_name="Reply-to tutor")
    reply_to_assigner = models.BooleanField(default=False, verbose_name="Reply-to detention assigner")
    
    MAIL_TYPE_CHOICES = (('', 'None'), ('to', 'To'), ('cc', 'Cc'), ('bcc', 'Bcc'))
    MAIL_TYPE_CHOICES_LENGTH = max([len(item[0]) for item in MAIL_TYPE_CHOICES])
    
    advisor_mail = models.CharField(max_length=MAIL_TYPE_CHOICES_LENGTH, choices=MAIL_TYPE_CHOICES, blank=True, verbose_name='Advisor e-mail')
    tutor_mail = models.CharField(max_length=MAIL_TYPE_CHOICES_LENGTH, choices=MAIL_TYPE_CHOICES, blank=True, verbose_name='Tutor e-mail')
    assigner_mail = models.CharField(max_length=MAIL_TYPE_CHOICES_LENGTH, choices=MAIL_TYPE_CHOICES, blank=True, verbose_name='Assigner e-mail')
    
    do_not_send_same_day_before = models.TimeField(blank=True, null=True)
    
    middle_section = models.TextField()
    botton_section = models.TextField()
    
    skip_processing_before = models.DateField(blank=True, null=True)
    
class DetentionCC(models.Model):
    mailer = models.ForeignKey(DetentionMailer, on_delete=models.CASCADE)
    address = models.EmailField(max_length=254)
    
    MAIL_TYPE_CHOICES = (('to', 'To'), ('cc', 'Cc'), ('bcc', 'Bcc'))
    MAIL_TYPE_CHOICES_LENGTH = max([len(item[0]) for item in MAIL_TYPE_CHOICES])
    
    mail_type = models.CharField(max_length=MAIL_TYPE_CHOICES_LENGTH, choices=MAIL_TYPE_CHOICES)
    
    class Meta:
        verbose_name="Additional address"
        verbose_name_plural = "Additional addresses"
        
        unique_together = (('mailer', 'address'), )
    
    def __str__(self):
        return "{mail_type:} {email:}".format(mail_type=self.get_mail_type_display(), email=self.address)

class DetentionTo(models.Model):
    FAMILY_CHOICES = (('IDFamily1', 'Family 1'), ('IDFamily2', 'Family 2'), ('IDFamily3', 'Family 3'), ('IDFamily4', 'Family 4'))
    PARENT_CHOICES = (('a', 'Parent A'), ('b', 'Parent B'))
    
    FAMILY_CHOICES_LENGTH = max([len(item[0]) for item in FAMILY_CHOICES])
    PARENT_CHOICES_LENGTH = max([len(item[0]) for item in FAMILY_CHOICES])
    
    mailer = models.ForeignKey(DetentionMailer, on_delete=models.CASCADE)
    
    family_id_key = models.CharField(max_length=FAMILY_CHOICES_LENGTH, choices=FAMILY_CHOICES, verbose_name="Family")
    parent_code = models.CharField(max_length=PARENT_CHOICES_LENGTH, choices=PARENT_CHOICES, verbose_name="Parent Code")
    
    class Meta:
        unique_together = (('family_id_key', 'parent_code'), )
    
    def __str__(self):
        return self.family_id_key + " P" + self.parent_code

class DetentionErrorNotification(models.Model):
    mailer = models.ForeignKey(DetentionMailer, on_delete=models.CASCADE)
    address = models.EmailField(max_length=254)
    
    class Meta:
        verbose_name = "Error recipient"
        
        unique_together = (('mailer', 'address'), )
    
    def __str__(self):
        return self.address

class Detention(models.Model):
    incident_id = models.PositiveIntegerField(unique=True)
    detention_date = models.DateField(null=True)
    code = models.ForeignKey(Code, on_delete=models.CASCADE)
    offense = models.ForeignKey(Offense, null=True, on_delete=models.CASCADE)
    comments = models.TextField(blank=True)
    
    term = models.ForeignKey(Term, null=True, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, null=True, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, null=True, on_delete=models.CASCADE)
    
    sent = models.BooleanField(default=False)
    
    def __str__(self):
        return "Detention {}".format(self.incident_id)