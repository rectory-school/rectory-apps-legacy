from django.db import models

class TeacherManager(models.Manager):
    def get_queryset(self):
        return super(TeacherManager, self).get_queryset().select_related('academic_teacher')


class EnrichmentOptionManager(models.Manager):
    def get_queryset(self):
        return super(EnrichmentOptionManager, self).get_queryset().select_related('teacher', 'teacher__academic_teacher')

class EnrichmentSignupManager(models.Manager):
    def get_queryset(self):
        return super(EnrichmentSignupManager, self).get_queryset().select_related('student', 'student__academic_student', 'enrichment_option', 'enrichment_option__teacher', 'enrichment_option__teacher__academic_teacher')