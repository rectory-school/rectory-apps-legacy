# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('academics', '0018_student_username'),
    ]

    operations = [
        migrations.AddField(
            model_name='enrollment',
            name='enrolled_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
