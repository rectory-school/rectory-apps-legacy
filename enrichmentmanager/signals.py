from django.db.models.signals import post_save
from enrichmentmanager.models import EnrichmentSlot, Teacher, EnrichmentOption
from django.dispatch import receiver

@receiver(post_save, sender=EnrichmentSlot)
def createEnrichmentOptions(sender, instance, created, *args, **kwargs):
    if created:
        for teacher in Teacher.objects.exclude(default_room=""):
            EnrichmentOption(slot=instance, teacher=teacher, location=teacher.default_room).save()