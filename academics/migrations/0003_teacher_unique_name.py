# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('academics', '0002_teacher_prefix'),
    ]

    operations = [
        migrations.AddField(
            model_name='teacher',
            name='unique_name',
            field=models.CharField(default=None, max_length=255, unique=True),
            preserve_default=False,
        ),
    ]
