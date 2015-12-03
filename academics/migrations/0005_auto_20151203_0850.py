# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('academics', '0004_auto_20151203_0834'),
    ]

    operations = [
        migrations.AlterField(
            model_name='teacher',
            name='teacher_id',
            field=models.CharField(max_length=5, unique=True),
        ),
    ]
