# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('academics', '0003_teacher_unique_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='teacher',
            name='teacher_id',
            field=models.CharField(max_length=4, unique=True),
        ),
    ]
