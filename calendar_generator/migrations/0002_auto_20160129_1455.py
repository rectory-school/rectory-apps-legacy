# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calendar_generator', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='day',
            options={'ordering': ['day_order']},
        ),
        migrations.AddField(
            model_name='skipdate',
            name='end_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
