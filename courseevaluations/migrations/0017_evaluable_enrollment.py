# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('academics', '0020_historicalacademicyear_historicalcourse_historicaldorm_historicalenrollment_historicalsection_histor'),
        ('courseevaluations', '0016_auto_20151214_1500'),
    ]

    operations = [
        migrations.AddField(
            model_name='evaluable',
            name='enrollment',
            field=models.ForeignKey(to='academics.Enrollment', null=True),
        ),
    ]
