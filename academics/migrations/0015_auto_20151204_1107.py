# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('academics', '0014_auto_20151204_0901'),
    ]

    operations = [
        migrations.AddField(
            model_name='enrollment',
            name='status_attending',
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AddField(
            model_name='enrollment',
            name='status_enrollment',
            field=models.CharField(blank=True, max_length=20),
        ),
    ]
