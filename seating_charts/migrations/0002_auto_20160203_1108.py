# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('seating_charts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='seatingstudent',
            name='foodAllergy',
            field=models.CharField(verbose_name='Food allergy status', default='', max_length=7, blank=True, choices=[('', 'No Allergies'), ('ALLERGY', 'Allergy'), ('EPIPEN', 'Allergy (EpiPen)')]),
        ),
        migrations.AlterField(
            model_name='seatingstudent',
            name='ethnicity',
            field=models.ForeignKey(blank=True, null=True, to='seating_charts.Ethnicity', on_delete=models.CASCADE),
        ),
    ]
