# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('academics', '0005_auto_20151203_0850'),
    ]

    operations = [
        migrations.AlterField(
            model_name='teacher',
            name='unique_name',
            field=models.CharField(max_length=255),
        ),
    ]
